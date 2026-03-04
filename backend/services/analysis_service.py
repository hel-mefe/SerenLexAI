from __future__ import annotations

import io
import uuid
from typing import Optional

import pdfplumber
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


class DocumentTooLongError(ValueError):
    """Raised when the document exceeds the maximum allowed page count."""

    def __init__(self, pages: int, max_pages: int) -> None:
        self.pages = pages
        self.max_pages = max_pages
        super().__init__(
            f"Document exceeds maximum allowed size ({max_pages} pages). "
            f"Your document has {pages} pages."
        )


class DocumentExtractionError(ValueError):
    """Raised when text extraction from the document fails."""

    pass


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

    def create_analysis_from_upload(
        self,
        file_content: bytes,
        filename: str,
        title: str,
        max_pages: int,
    ) -> AnalysisDetail:
        """
        Create an analysis from an uploaded PDF. Validates page count and
        extracts text. Raises DocumentTooLongError or DocumentExtractionError
        on validation failure.
        """
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            num_pages = len(pdf.pages)
            if num_pages > max_pages:
                raise DocumentTooLongError(num_pages, max_pages)
            try:
                parts: list[str] = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        parts.append(text)
                raw_text = "\n\n".join(parts).strip() if parts else ""
            except Exception as e:
                raise DocumentExtractionError(
                    f"Could not extract text from the document: {e!s}"
                ) from e

        payload = AnalysisCreate(
            title=title or filename or "Uploaded document",
            original_filename=filename,
            source_type="upload",
            raw_text=raw_text or None,
        )
        return self.create_analysis(payload)

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

