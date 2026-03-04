from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.models.domain import NodeErrorModel, RecommendationModel
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
    if state.fatal_error:
        return state

    classified = state.classified_clauses or []
    errors: list[NodeErrorModel] = list(state.errors or [])

    risky_clauses = [
        c for c in classified if (c.risk_level or "").lower() in {"high", "critical"}
    ]

    if not risky_clauses:
        return state.model_copy(update={"recommendations": [], "errors": errors})

    settings = get_settings()
    raw_llm = ChatOpenAI(
        model=settings.primary_llm,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    llm = raw_llm.with_structured_output(RecommendationOutput)

    recommendations: List[RecommendationModel] = []

    for clause in risky_clauses:
        clause_ref = clause.clause_type or "clause"
        payload = {
            "clause": {
                "clause_type": clause.clause_type,
                "section_type": clause.section_type,
                "text": clause.extracted_text,
                "risk_level": clause.risk_level,
                "risk_score": clause.risk_score,
                "risk_rationale": clause.risk_rationale,
                "page_start": clause.page_start,
                "page_end": clause.page_end,
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
                RecommendationModel(
                    clause_ref=result.clause_ref or clause_ref,
                    recommendation_text=result.recommendation_text,
                    suggested_language=result.suggested_language,
                    priority=priority,
                    clause_type=clause.clause_type,
                    section_type=clause.section_type,
                )
            )
        except Exception as exc:
            errors.append(
                NodeErrorModel(
                    node="recommender",
                    clause_id=clause.chunk_id,
                    error_type="recommendation_failed",
                    message=str(exc),
                )
            )

    return state.model_copy(update={"recommendations": recommendations, "errors": errors})

