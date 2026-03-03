from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.actions import Action
from repositories.analysis_repository import AnalysisRepository
from repositories.clause_repository import ClauseRepository
from repositories.action_repository import ActionRepository
from schemas.analysis import (
    AnalysisCreate,
    AnalysisDetail,
    AnalysisListItem,
    AnalysisListResponse,
)
from schemas.actions import ActionCreate


class AnalysisService:
    """
    Application service for analysis-related operations.
    Encapsulates domain logic on top of repositories.
    """

    def __init__(
        self,
        db: Session,
        analysis_repository: AnalysisRepository,
        clause_repository: ClauseRepository,
        action_repository: ActionRepository,
    ) -> None:
        self._db = db
        self._analyses = analysis_repository
        self._clauses = clause_repository
        self._actions = action_repository

    def list_analyses(
        self,
        *,
        search: Optional[str],
        risk: Optional[str],
        page: int,
        page_size: int,
    ) -> AnalysisListResponse:
        analyses, total = self._analyses.list_paginated(
            search=search,
            risk=risk,
            page=page,
            page_size=page_size,
        )

        items: list[AnalysisListItem] = []
        for a in analyses:
            clauses_count = (
                a.flagged_count
                or self._analyses.count_clauses(a.id)
            )

            items.append(
                AnalysisListItem(
                    id=a.id,
                    name=a.title,
                    date=a.created_at,
                    risk=a.overall_risk,
                    clauses=clauses_count,
                    score=a.risk_score or 0,
                )
            )

        return AnalysisListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_analysis(self, analysis_id: uuid.UUID) -> AnalysisDetail:
        analysis = self._analyses.get(analysis_id)
        if not analysis:
            raise ValueError("Analysis not found")

        return AnalysisDetail(
            id=analysis.id,
            title=analysis.title,
            original_filename=analysis.original_filename,
            source_type=analysis.source_type,
            status=analysis.status,
            overall_risk=analysis.overall_risk,
            risk_score=analysis.risk_score,
            flagged_count=analysis.flagged_count,
            high_count=analysis.high_count,
            medium_count=analysis.medium_count,
            low_count=analysis.low_count,
            created_at=analysis.created_at,
            updated_at=analysis.updated_at,
        )

    def create_analysis(self, payload: AnalysisCreate) -> AnalysisDetail:
        analysis = Analysis(
            title=payload.title,
            original_filename=payload.original_filename,
            source_type=payload.source_type,
            status="pending",
            raw_text=payload.raw_text,
        )

        self._analyses.create(analysis)

        # Log an upload / creation event for history
        action_payload = ActionCreate(
            type="UPLOAD",
            title="Contract Uploaded",
            description=payload.title,
            analysis_id=analysis.id,
            metadata={
                "source_type": payload.source_type,
                "original_filename": payload.original_filename,
            },
        )
        self._log_action(action_payload)

        self._db.commit()

        return self.get_analysis(analysis.id)

    def _log_action(self, payload: ActionCreate) -> Action:
        action = Action(
            type=payload.type,
            title=payload.title,
            description=payload.description,
            analysis_id=payload.analysis_id,
            user_id=payload.user_id,
            meta=payload.metadata,
        )
        return self._actions.log(action)

