from __future__ import annotations

from typing import Any, Dict, List

from app.contract_intelligence.state import ContractState
from app.contract_intelligence.tools.scorer import compute_overall_score


async def score_calculator_node(state: ContractState) -> ContractState:
    if state.get("fatal_error"):
        return state

    clauses: List[Dict[str, Any]] = list(state.get("classified_clauses") or [])
    errors = list(state.get("errors") or [])

    try:
        score, level, breakdown = compute_overall_score(clauses)
    except Exception as exc:
        errors.append(
            {
                "node": "score_calculator",
                "clause_id": None,
                "error_type": "score_calculation_failed",
                "message": str(exc),
            }
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

    new_state: ContractState = dict(state)
    new_state["risk_score"] = score
    new_state["risk_level"] = level  # type: ignore[assignment]
    new_state["score_breakdown"] = breakdown
    new_state["errors"] = errors
    return new_state

