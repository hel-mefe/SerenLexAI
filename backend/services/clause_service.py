from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from repositories.clause_repository import ClauseRepository
from schemas.analysis import SeverityLevel
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
        # Normalize incoming severity (e.g. 'High' | 'Medium' | 'Low') to the
        # lowercase values stored in the database ('low', 'medium', 'high', 'critical').
        severity_db: Optional[str] = None
        if severity:
            value = severity.lower()
            if value in {"low", "medium", "high", "critical"}:
                severity_db = value

        clauses, total = self._clauses.list_by_analysis(
            analysis_id=analysis_id,
            severity=severity_db,
        )

        return ClauseListResponse(
            items=[
                ClauseRead(
                    id=c.id,
                    title=c.title,
                    # Map DB severity (low/medium/high/critical) to UI SeverityLevel.
                    severity=self._map_severity(c.severity),
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

    @staticmethod
    def _map_severity(value: str | None) -> SeverityLevel:
        """
        Normalize DB severity string to UI SeverityLevel.

        - 'high' and 'critical' -> 'High'
        - 'medium'             -> 'Medium'
        - anything else / None -> 'Low'
        """
        if not value:
            return "Low"
        v = value.lower()
        if v in {"high", "critical"}:
            return "High"
        if v == "medium":
            return "Medium"
        return "Low"