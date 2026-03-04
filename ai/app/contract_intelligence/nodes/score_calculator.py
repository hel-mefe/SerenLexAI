from __future__ import annotations

from typing import Any, Dict, List

from app.contract_intelligence.models.domain import NodeErrorModel
from app.contract_intelligence.state import ContractState
from app.contract_intelligence.tools.scorer import compute_overall_score


async def score_calculator_node(state: ContractState) -> ContractState:
    if state.fatal_error:
        return state

    clauses: List[Dict[str, Any]] = [
        c.model_dump() for c in (state.classified_clauses or [])
    ]
    errors: list[NodeErrorModel] = list(state.errors or [])

    try:
        score, level, breakdown = compute_overall_score(clauses)
    except Exception as exc:
        errors.append(
            NodeErrorModel(
                node="score_calculator",
                clause_id=None,
                error_type="score_calculation_failed",
                message=str(exc),
            )
        )
        score = 0.0
        level = "low"
        breakdown = {
            "by_section": {},
            "top_risks": [],
            "clause_count": len(clauses),
            "high_risk_count": 0,
            "critical_risk_count": 0,
        }

    return state.model_copy(
        update={
            "risk_score": float(score),
            "risk_level": level,  # type: ignore[assignment]
            "score_breakdown": breakdown,
            "errors": errors,
        }
    )

