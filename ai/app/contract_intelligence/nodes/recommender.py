from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.prompts.recommender import (
    RECOMMENDER_SYSTEM_PROMPT,
)
from app.contract_intelligence.state import ContractState


class RecommendationOutput(BaseModel):
    clause_ref: str
    recommendation_text: str
    suggested_language: str
    priority: str


async def recommender_node(state: ContractState) -> ContractState:
    if state.get("fatal_error"):
        return state

    classified = state.get("classified_clauses") or []
    errors = list(state.get("errors") or [])

    risky_clauses: List[Dict[str, Any]] = []
    for clause in classified:
        level = (clause.get("risk_level") or "").lower()
        if level in {"high", "critical"}:
            risky_clauses.append(clause)

    if not risky_clauses:
        new_state: ContractState = dict(state)
        new_state["recommendations"] = []
        new_state["errors"] = errors
        return new_state

    settings = get_settings()
    raw_llm = ChatOpenAI(
        model=settings.primary_llm,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    llm = raw_llm.with_structured_output(RecommendationOutput)

    recommendations: List[Dict[str, Any]] = []

    for clause in risky_clauses:
        clause_ref = clause.get("clause_number") or clause.get("clause_type") or "clause"
        payload = {
            "clause": {
                "clause_type": clause.get("clause_type"),
                "section_type": clause.get("section_type"),
                "text": clause.get("extracted_text"),
                "risk_level": clause.get("risk_level"),
                "risk_score": clause.get("risk_score"),
                "risk_rationale": clause.get("risk_rationale"),
                "page_start": clause.get("page_start"),
                "page_end": clause.get("page_end"),
            },
            "jurisdiction": None,
        }

        try:
            result: RecommendationOutput = await llm.ainvoke(
                {
                    "role": "user",
                    "content": {
                        "system": RECOMMENDER_SYSTEM_PROMPT,
                        "payload": payload,
                    },
                }
            )
            priority = result.priority
            if priority not in {"must_fix", "should_fix", "consider_fixing"}:
                priority = "should_fix"
            recommendations.append(
                {
                    "clause_ref": result.clause_ref or clause_ref,
                    "recommendation_text": result.recommendation_text,
                    "suggested_language": result.suggested_language,
                    "priority": priority,
                    "clause_type": clause.get("clause_type"),
                    "section_type": clause.get("section_type"),
                }
            )
        except Exception as exc:
            errors.append(
                {
                    "node": "recommender",
                    "clause_id": clause.get("chunk_id"),
                    "error_type": "recommendation_failed",
                    "message": str(exc),
                }
            )

    new_state: ContractState = dict(state)
    new_state["recommendations"] = recommendations
    new_state["errors"] = errors
    return new_state

