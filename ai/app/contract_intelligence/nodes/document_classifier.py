"""
Document type classifier: determines if the document is a legal contract or not.
If not_contract, the pipeline will skip clause analysis and persist an early result.
"""

from __future__ import annotations

MAX_PREVIEW_CHARS = 6000

from langchain_openai import ChatOpenAI

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.models.domain import NodeErrorModel
from app.contract_intelligence.prompts.document_classifier import (
    DOCUMENT_CLASSIFIER_SYSTEM_PROMPT,
    DOCUMENT_CLASSIFIER_USER_TEMPLATE,
)
from app.contract_intelligence.state import ContractState


def _text_preview(state: ContractState) -> str:
    """Build a single string from raw input or normalized chunks for classification."""
    raw = state.raw_input
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="replace")
    if raw and len(raw.strip()) > 0:
        return (raw.strip()[:MAX_PREVIEW_CHARS] + ("..." if len(raw) > MAX_PREVIEW_CHARS else "")) or ""
    chunks = state.normalized_chunks or state.chunks
    if chunks:
        parts = []
        total = 0
        for c in chunks:
            content = (c.content or "").strip()
            if not content:
                continue
            if total + len(content) > MAX_PREVIEW_CHARS:
                parts.append(content[: MAX_PREVIEW_CHARS - total] + "...")
                break
            parts.append(content)
            total += len(content)
        return "\n".join(parts) if parts else ""
    return ""


async def document_classifier_node(state: ContractState) -> ContractState:
    """Classify document as contract or not_contract; set state.document_type and document_type_reason."""
    try:
        text = _text_preview(state)
        if not text or len(text.strip()) < 50:
            return state.model_copy(
                update={
                    "document_type": "not_contract",
                    "document_type_reason": "Document has insufficient text to classify.",
                }
            )
        settings = get_settings()
        llm = ChatOpenAI(
            model=settings.fast_llm,
            temperature=0,
            api_key=settings.openai_api_key,
        )
        user_msg = DOCUMENT_CLASSIFIER_USER_TEMPLATE.format(text_preview=text)
        response = await llm.ainvoke(
            [{"role": "system", "content": DOCUMENT_CLASSIFIER_SYSTEM_PROMPT}, {"role": "user", "content": user_msg}]
        )
        content = (response.content or "").strip().lower()
        if "not_contract" in content or "not contract" in content:
            doc_type = "not_contract"
            reason = content if len(content) < 500 else (content[:497] + "...")
        else:
            doc_type = "contract"
            reason = "Document classified as a legal contract." if not content else content[:500]
        return state.model_copy(
            update={
                "document_type": doc_type,
                "document_type_reason": reason or None,
            }
        )
    except Exception as exc:
        error = NodeErrorModel(
            node="document_classifier",
            error_type="classification_failed",
            message=str(exc),
        )
        return state.model_copy(
            update={
                "errors": [*state.errors, error],
                "document_type": "contract",
                "document_type_reason": f"Classification failed: {exc}; proceeding as contract.",
            }
        )
