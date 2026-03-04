"""
Syncs workflow result into UI entities (analyses, clauses, actions).

Single source of truth for CRUD and event-sourcing; all methods under 25 lines.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.models.domain import ClassifiedClauseModel, RecommendationModel
from app.contract_intelligence.models.ui_entities import Action, Analysis, Clause
from app.contract_intelligence.state import ContractState


def _severity_from_level(level: Optional[str]) -> str:
    if not level or level not in ("low", "medium", "high", "critical"):
        return "low"
    return level


def _recommendation_for_clause(
    clause: ClassifiedClauseModel,
    recommendations: list[RecommendationModel],
) -> str:
    for rec in recommendations:
        if rec.clause_type == clause.clause_type and rec.section_type == clause.section_type:
            parts = [rec.recommendation_text or ""]
            if rec.suggested_language:
                parts.append(f" Suggested: {rec.suggested_language}")
            return "".join(parts).strip() or "Review and negotiate as needed."
    return clause.risk_rationale or "Review clause."


def _counts_from_state(state: ContractState) -> tuple[int, int, int, int]:
    low = medium = high = critical = 0
    for cl in state.classified_clauses:
        level = (cl.risk_level or "").lower()
        if level == "low":
            low += 1
        elif level == "medium":
            medium += 1
        elif level == "high":
            high += 1
        elif level == "critical":
            critical += 1
    flagged = high + critical
    return flagged, high, medium, low


async def emit_action(
    session: AsyncSession,
    analysis_id: uuid.UUID,
    user_id: Optional[uuid.UUID],
    action_type: str,
    title: str,
    description: str,
    meta: Optional[dict] = None,
) -> None:
    action = Action(
        analysis_id=analysis_id,
        user_id=user_id,
        type=action_type,
        title=title,
        description=description,
        meta=meta,
    )
    session.add(action)


async def update_analysis_from_state(
    session: AsyncSession,
    analysis_id: str,
    state: ContractState,
) -> None:
    row = await session.get(Analysis, uuid.UUID(analysis_id))
    if not row:
        return
    flagged, high, medium, low = _counts_from_state(state)
    row.status = "failed" if state.fatal_error else ("partial" if state.errors else "completed")
    row.overall_risk = state.risk_level
    row.risk_score = int(round(state.risk_score)) if state.risk_score is not None else None
    row.flagged_count = flagged
    row.high_count = high
    row.medium_count = medium
    row.low_count = low
    raw_parts = [b.text for b in state.extracted_blocks]
    row.raw_text = "\n".join(raw_parts).strip() if raw_parts else None


async def upsert_clauses_for_analysis(
    session: AsyncSession,
    analysis_id: str,
    state: ContractState,
) -> None:
    aid = uuid.UUID(analysis_id)
    existing = await session.scalars(select(Clause).where(Clause.analysis_id == aid))
    for c in existing:
        await session.delete(c)
    for idx, cl in enumerate(state.classified_clauses):
        rec_text = _recommendation_for_clause(cl, state.recommendations)
        severity = _severity_from_level(cl.risk_level)
        title = cl.clause_type or "Clause"
        if len(title) > 255:
            title = title[:252] + "..."
        session.add(
            Clause(
                analysis_id=aid,
                title=title,
                severity=severity,
                original_text=cl.extracted_text or "",
                risk_explanation=cl.risk_rationale or "",
                recommended_action=rec_text,
                clause_type=cl.clause_type,
                position_index=idx,
            )
        )


async def sync_workflow_result_to_ui(
    session: AsyncSession,
    state: ContractState,
    analysis_id: str,
    user_id: Optional[str] = None,
) -> None:
    """
    Persist workflow result into analyses/clauses and emit final Action.
    Call after run_contract_analysis.
    """
    aid = uuid.UUID(analysis_id)
    uid = uuid.UUID(user_id) if user_id else None
    await update_analysis_from_state(session, analysis_id, state)
    await upsert_clauses_for_analysis(session, analysis_id, state)
    if state.fatal_error or state.errors:
        await emit_action(
            session,
            aid,
            uid,
            "FAILED",
            "Processing failed",
            state.fatal_error or "One or more steps reported errors.",
            meta={"errors": [e.model_dump() for e in state.errors]},
        )
    else:
        await emit_action(
            session,
            aid,
            uid,
            "COMPLETED",
            "Processing completed",
            f"Risk: {state.risk_level}; score {state.risk_score}.",
            meta={"risk_score": state.risk_score, "clause_count": len(state.classified_clauses)},
        )
