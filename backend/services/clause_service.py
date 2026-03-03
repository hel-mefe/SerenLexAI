from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from repositories.clause_repository import ClauseRepository
from schemas.clauses import ClauseListResponse, ClauseRead


class ClauseService:
    def __init__(
        self,
        db: Session,
        clause_repository: ClauseRepository,
    ) -> None:
        self._db = db
        self._clauses = clause_repository

    def list_for_analysis(
        self,
        analysis_id: uuid.UUID,
        *,
        severity: Optional[str] = None,
    ) -> ClauseListResponse:
        clauses, total = self._clauses.list_by_analysis(
            analysis_id=analysis_id,
            severity=severity,
        )

        return ClauseListResponse(
            items=[
                ClauseRead(
                    id=c.id,
                    title=c.title,
                    severity=c.severity,  # type: ignore[arg-type]
                    original_text=c.original_text,
                    risk_explanation=c.risk_explanation,
                    recommended_action=c.recommended_action,
                    clause_type=c.clause_type,
                    position_index=c.position_index,
                )
                for c in clauses
            ],
            total=total,
        )

