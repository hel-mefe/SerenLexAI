from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from contract_ai.infrastructure.db import SessionLocal
from contract_ai.infrastructure.models import Analysis, Clause


def persist_results_node(state):
    """
    Persist the final analysis and clause results into the SerenLex Postgres DB.

    This node assumes the backend has already created an `analyses` row with
    the given analysis_id. It updates that row's risk fields and inserts one
    `clauses` row per clause_result in the state.
    """
    db: Session = SessionLocal()

    analysis_id_str = state.get("analysis_id")
    if not analysis_id_str:
        return state

    try:
        analysis_id = uuid.UUID(analysis_id_str)
    except (TypeError, ValueError):
        # Invalid UUID; nothing to persist
        return state

    analysis = db.get(Analysis, analysis_id)
    if not analysis:
        # Backend hasn't created the analysis row (or DB mismatch); bail out
        return state

    # Classifier sets is_contract (bool). Treat False or string "false" as not a contract.
    raw = state.get("is_contract", True)
    is_contract = raw is True or (isinstance(raw, str) and raw.lower() == "true")

    if not is_contract:
        # Document was classified as not a contract: no risk, no score, no clauses
        analysis.status = "not_contract"
        analysis.overall_risk = None
        analysis.risk_score = None
        analysis.flagged_count = 0
        analysis.high_count = 0
        analysis.medium_count = 0
        analysis.low_count = 0
        # Do not insert any clause rows
    else:
        # Normal contract: persist risk and clauses
        analysis.status = "completed"
        analysis.overall_risk = state.get("overall_risk")
        analysis.risk_score = state.get("risk_score")
        analysis.flagged_count = state.get("flagged_count", 0) or 0
        analysis.high_count = state.get("high_count", 0) or 0
        analysis.medium_count = state.get("medium_count", 0) or 0
        analysis.low_count = state.get("low_count", 0) or 0

        for result in state.get("clause_results", []):
            clause = Clause(
                analysis_id=analysis_id,
                title=result.title,
                severity=result.severity,
                original_text=result.original_text,
                risk_explanation=result.risk_explanation,
                recommended_action=result.recommended_action,
                clause_type=result.clause_type,
                position_index=result.position_index,
            )
            db.add(clause)

    db.commit()
    db.close()

    return state