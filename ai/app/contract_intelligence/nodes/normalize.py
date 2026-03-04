from __future__ import annotations

import re
from typing import List, Set

from app.contract_intelligence.models.domain import BlockModel, ChunkModel, NodeErrorModel
from app.contract_intelligence.state import ContractState


HEADER_FOOTER_MAX_LEN = 120
MIN_HEADER_FOOTER_REPEAT = 0.4  # fraction of pages


def _normalize_text(value: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\ufb01": "fi",
        "\ufb02": "fl",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"\n{3,}", "\n\n", value).strip()


def _detect_repeating_lines(blocks: List[BlockModel], page_count: int) -> Set[str]:
    counts: dict[str, set[int]] = {}
    for block in blocks:
        text = block.text.strip()
        if not text or len(text) > HEADER_FOOTER_MAX_LEN:
            continue
        counts.setdefault(text, set()).add(block.page_number)
    threshold = max(int(page_count * MIN_HEADER_FOOTER_REPEAT), 2)
    return {text for text, pages in counts.items() if len(pages) >= threshold}


PAGE_NUMBER_PATTERNS = [
    re.compile(r"^page\s+\d+(\s+of\s+\d+)?$", re.IGNORECASE),
    re.compile(r"^\d+\s*/\s*\d+$"),
]


def _looks_like_page_number(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    return any(pat.match(stripped) for pat in PAGE_NUMBER_PATTERNS)


def _has_annotation(text: str) -> bool:
    lowered = text.lower()
    tokens = ["track changes", "inserted text", "[deleted]", "[added]", "[amended]"]
    if any(token in lowered for token in tokens):
        return True
    return ">>" in text or "<<" in text


def _strip_headers_and_footers(content: str, repeating: Set[str]) -> str:
    kept: List[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        upper = stripped.upper()
        if stripped in repeating:
            continue
        if _looks_like_page_number(stripped):
            continue
        if upper in {"DRAFT", "CONFIDENTIAL"}:
            continue
        kept.append(line)
    return "\n".join(kept)


def _normalize_chunk(chunk: ChunkModel, repeating: Set[str]) -> ChunkModel:
    stripped = _strip_headers_and_footers(chunk.content, repeating)
    cleaned = _normalize_text(stripped)
    has_annotation = chunk.has_annotation or _has_annotation(chunk.content or "")
    return chunk.model_copy(update={"content": cleaned, "has_annotation": has_annotation})


async def normalize_node(state: ContractState) -> ContractState:
    try:
        repeating = _detect_repeating_lines(state.extracted_blocks, state.page_count)
        normalized = [_normalize_chunk(chunk, repeating) for chunk in state.chunks]
        return state.model_copy(update={"normalized_chunks": normalized})
    except Exception as exc:
        error = NodeErrorModel(
            node="normalize",
            error_type="normalize_failed",
            message=str(exc),
        )
        return state.model_copy(
            update={"errors": [*state.errors, error], "normalized_chunks": state.chunks}
        )

