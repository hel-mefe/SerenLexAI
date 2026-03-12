from __future__ import annotations

import io
import uuid
from pathlib import Path
from typing import Optional

import pdfplumber
from sqlalchemy.orm import Session

from ai.tasks import enqueue_contract_analysis
from core.config import settings
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
    RiskLevel,
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

    @staticmethod
    def _normalize_risk(level: Optional[str]) -> Optional[RiskLevel]:
        """
        Normalize risk strings coming from the DB / AI worker into
        the UI enum: 'High' | 'Medium' | 'Low'.

        - Accepts lower/upper case (e.g. 'high', 'HIGH').
        - Maps 'critical' to 'High' for display purposes.
        - Returns None for unknown/empty values.
        """
        if not level:
            return None
        value = level.lower()
        if value in {"high", "critical"}:
            return "High"
        if value == "medium":
            return "Medium"
        if value == "low":
            return "Low"
        return None

    def list_analyses(
        self,
        *,
        search: Optional[str],
        risk: Optional[str],
        page: int,
        page_size: int,
    ) -> AnalysisListResponse:
        # Normalise incoming risk filter so it matches how values are stored in DB.
        # DB stores overall_risk as lowercase strings ('high', 'medium', 'low').
        risk_normalized: Optional[str] = None
        if risk:
            value = risk.lower()
            if value in {"high", "medium", "low"}:
                risk_normalized = value

        analyses, total = self._analyses.list_paginated(
            search=search,
            risk=risk_normalized,
            page=page,
            page_size=page_size,
        )

        items: list[AnalysisListItem] = []
        for a in analyses:
            clauses_count = (
                a.flagged_count
                or self._analyses.count_clauses(a.id)
            )
            # Not-a-contract analyses have no risk, no score
            is_not_contract = (a.status or "").lower() == "not_contract"
            risk = None if is_not_contract else self._normalize_risk(a.overall_risk)
            score = 0 if is_not_contract else (a.risk_score or 0)

            items.append(
                AnalysisListItem(
                    id=a.id,
                    name=a.title,
                    date=a.created_at,
                    risk=risk,
                    clauses=clauses_count,
                    score=score,
                    status=a.status,
                )
            )

        return AnalysisListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_analysis_pdf_path(self, analysis_id: uuid.UUID) -> Optional[Path]:
        """
        Return the path to the stored PDF for this analysis, if it was
        created from an upload and the file exists.
        """
        analysis = self._analyses.get(analysis_id)
        if not analysis or analysis.source_type != "upload":
            return None
        path = Path(settings.UPLOAD_DIR) / f"{analysis_id}.pdf"
        return path if path.is_file() else None

    def get_analysis_report_pdf_path(self, analysis_id: uuid.UUID) -> Optional[Path]:
        """
        Return the path to the generated risk report PDF for this analysis,
        if the analysis is completed and the report file exists.
        """
        analysis = self._analyses.get(analysis_id)
        if not analysis or analysis.status != "completed":
            return None
        path = Path(settings.REPORTS_DIR) / f"{analysis_id}_risk_report.pdf"
        return path if path.is_file() else None

    def get_analysis(self, analysis_id: uuid.UUID) -> AnalysisDetail:
        analysis = self._analyses.get(analysis_id)
        if not analysis:
            raise ValueError("Analysis not found")

        # Not-a-contract analyses: no risk, no score, zero counts
        is_not_contract = (analysis.status or "").lower() == "not_contract"
        overall_risk = None if is_not_contract else self._normalize_risk(analysis.overall_risk)
        risk_score = None if is_not_contract else analysis.risk_score
        flagged = 0 if is_not_contract else (analysis.flagged_count or 0)
        high_c = 0 if is_not_contract else (analysis.high_count or 0)
        medium_c = 0 if is_not_contract else (analysis.medium_count or 0)
        low_c = 0 if is_not_contract else (analysis.low_count or 0)

        return AnalysisDetail(
            id=analysis.id,
            title=analysis.title,
            original_filename=analysis.original_filename,
            source_type=analysis.source_type,
            status=analysis.status,
            overall_risk=overall_risk,
            risk_score=risk_score,
            flagged_count=flagged,
            high_count=high_c,
            medium_count=medium_c,
            low_count=low_c,
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

        # Fire-and-forget AI analysis via Redis/Celery
        enqueue_contract_analysis(analysis)

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
        extracts text. Saves the PDF to the shared uploads dir so the
        langgraph-ai worker can process it. Raises DocumentTooLongError or
        DocumentExtractionError on validation failure.
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

        # Create analysis record first to get ID
        analysis = Analysis(
            title=title or filename or "Uploaded document",
            original_filename=filename,
            source_type="upload",
            status="pending",
            raw_text=raw_text or None,
        )
        self._analyses.create(analysis)
        self._db.flush()

        # Save PDF to shared uploads dir for langgraph-ai worker (must be same path in worker container)
        upload_dir = Path(settings.UPLOAD_DIR).resolve()
        upload_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = upload_dir / f"{analysis.id}.pdf"
        pdf_path.write_bytes(file_content)

        # Log upload event
        self._log_action(
            ActionCreate(
                type="UPLOAD",
                title="Contract Uploaded",
                description=analysis.title,
                analysis_id=analysis.id,
                metadata={
                    "source_type": "upload",
                    "original_filename": filename,
                },
            )
        )

        self._db.commit()

        # Enqueue for langgraph-ai worker (uses shared /app/uploads volume)
        enqueue_contract_analysis(analysis, pdf_path=str(pdf_path))

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

