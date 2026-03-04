from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.models.domain import ClassifiedClauseModel, NodeErrorModel
from app.contract_intelligence.prompts.risk_classifier import (
    RISK_CLASSIFIER_SYSTEM_PROMPT,
)
from app.contract_intelligence.state import ContractState
from app.contract_intelligence.tools.embedder import embed_text
from app.contract_intelligence.tools.retriever import retrieve_similar_clauses


class RiskClassification(BaseModel):
    risk_level: str = Field(description="One of: low, medium, high, critical")
    risk_score: float = Field(description="Float from 1 to 10 inclusive")
    rationale: str


async def _classify_clause(
    llm: ChatOpenAI,
    session: AsyncSession,
    clause: Dict[str, Any],
    contract_context: Dict[str, Any],
) -> Dict[str, Any]:
    text = clause.get("extracted_text") or ""
    if not text.strip():
        return {
            **clause,
            "risk_level": None,
            "risk_score": None,
            "risk_rationale": None,
            "similar_precedents": [],
        }

    embedding = await embed_text(text)
    similar = await retrieve_similar_clauses(session=session, embedding=embedding)

    system_prompt = RISK_CLASSIFIER_SYSTEM_PROMPT

    payload = {
        "clause": {
            "clause_type": clause.get("clause_type"),
            "section_type": clause.get("section_type"),
            "text": text,
            "page_start": clause.get("page_start"),
            "page_end": clause.get("page_end"),
            "cross_references": clause.get("cross_references") or [],
        },
        "similar_clauses": similar,
        "contract_context": contract_context,
    }

    async def _invoke_with_retry(retries: int = 1) -> Optional[RiskClassification]:
        last_error: Optional[Exception] = None
        for _ in range(retries + 1):
            try:
                return await llm.ainvoke(
                    {
                        "role": "user",
                        "content": {
                            "system": system_prompt,
                            "payload": payload,
                        },
                    }
                )
            except Exception as exc:
                last_error = exc
        if last_error:
            raise last_error
        return None

    try:
        structured: RiskClassification = await _invoke_with_retry(retries=1)
        level = structured.risk_level.lower().strip()
        if level not in {"low", "medium", "high", "critical"}:
            level = "unknown"
        score = max(1.0, min(10.0, float(structured.risk_score)))
        rationale = structured.rationale.strip()
    except Exception:
        # Fallback when we cannot obtain structured output.
        level = "unknown"
        score = None
        rationale = None

    return {
        **clause,
        "risk_level": level,
        "risk_score": score,
        "risk_rationale": rationale,
        "similar_precedents": similar,
    }


async def risk_classifier_node_factory(
    session: AsyncSession,
):
    settings = get_settings()
    raw_llm = ChatOpenAI(
        model=settings.primary_llm,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    llm = raw_llm.with_structured_output(RiskClassification)

    async def node(state: ContractState) -> ContractState:
        if state.fatal_error:
            return state

        clauses_models = state.clauses or []
        clauses: list[Dict[str, Any]] = [
            c.model_dump() if isinstance(c, ClassifiedClauseModel) else dict(c)  # type: ignore[arg-type]
            for c in clauses_models
        ]
        errors: list[NodeErrorModel] = list(state.errors or [])

        # Basic contract-level context from metadata if provided.
        metadata = state.metadata or {}
        contract_context: Dict[str, Any] = {
            "contract_value": metadata.get("contract_value"),
            "currency": metadata.get("currency"),
            "other_metadata": metadata,
        }

        semaphore = asyncio.Semaphore(settings.max_concurrent_clause_tasks)

        async def wrapped(clause: Dict[str, Any]) -> Dict[str, Any]:
            if clause.get("clause_type") == "non_substantive":
                # Pass through, no risk classification.
                return {
                    **clause,
                    "risk_level": None,
                    "risk_score": None,
                    "risk_rationale": None,
                    "similar_precedents": [],
                }
            async with semaphore:
                try:
                    return await _classify_clause(
                        llm=llm,
                        session=session,
                        clause=clause,
                        contract_context=contract_context,
                    )
                except Exception as exc:
                    errors.append(
                        NodeErrorModel(
                            node="risk_classifier",
                            clause_id=str(clause.get("chunk_id") or ""),
                            error_type="risk_classification_failed",
                            message=str(exc),
                        )
                    )
                    return {
                        **clause,
                        "risk_level": "unknown",
                        "risk_score": None,
                        "risk_rationale": None,
                        "similar_precedents": [],
                    }

        tasks = [wrapped(c) for c in clauses]
        classified = await asyncio.gather(*tasks)

        classified_models = [ClassifiedClauseModel(**c) for c in classified]
        return state.model_copy(
            update={
                "classified_clauses": classified_models,
                "errors": errors,
            }
        )

    return node

