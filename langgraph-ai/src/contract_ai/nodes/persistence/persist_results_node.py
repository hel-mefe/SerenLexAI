from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.clauses import Clause
from core.database import SessionLocal


def persist_results_node(state):

    db: Session = SessionLocal()

    analysis_id = state["analysis_id"]

    analysis = db.get(Analysis, analysis_id)

    if not analysis:
        return state

    analysis.status = "completed"

    analysis.overall_risk = state.get("overall_risk")
    analysis.risk_score = state.get("risk_score")

    analysis.flagged_count = state.get("flagged_count", 0)
    analysis.high_count = state.get("high_count", 0)
    analysis.medium_count = state.get("medium_count", 0)
    analysis.low_count = state.get("low_count", 0)

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