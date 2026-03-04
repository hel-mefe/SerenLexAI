from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from core.config import settings
from core.dependencies import get_analysis_service, get_clause_service
from schemas.analysis import (
    AnalysisCreate,
    AnalysisDetail,
    AnalysisListResponse,
)
from schemas.clauses import ClauseListResponse
from services.analysis_service import (
    AnalysisService,
    DocumentExtractionError,
    DocumentTooLongError,
)
from services.clause_service import ClauseService


ALLOWED_CONTENT_TYPES = {"application/pdf"}
MAX_FILE_SIZE_BYTES = settings.UPLOAD_MAX_FILE_SIZE_MB * 1024 * 1024


router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get(
    "",
    response_model=AnalysisListResponse,
    summary="List analyses",
)
def list_analyses(
    search: Optional[str] = Query(
        default=None,
        description="Free-text search on analysis title",
    ),
    risk: Optional[str] = Query(
        default=None,
        description="Filter by overall risk level (High, Medium, Low)",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisListResponse:
    """
    Returns a paginated list of analyses, suitable for:
    - the Analyses table view
    - the Recent Analyses dashboard card (using a small page_size)
    """
    return service.list_analyses(
        search=search,
        risk=risk,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisDetail,
    summary="Get analysis details",
)
def get_analysis(
    analysis_id: uuid.UUID,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisDetail:
    """
    Returns a single analysis with its aggregate risk metrics.
    """
    try:
        return service.get_analysis(analysis_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )


@router.get(
    "/{analysis_id}/clauses",
    response_model=ClauseListResponse,
    summary="List clauses for an analysis",
)
def list_clauses_for_analysis(
    analysis_id: uuid.UUID,
    severity: Optional[str] = Query(
        default=None,
        description="Optional severity filter (High, Medium, Low)",
    ),
    service: ClauseService = Depends(get_clause_service),
) -> ClauseListResponse:
    """
    Returns all clauses for a given analysis, optionally filtered by severity.
    This powers the clause list and navigation on the Analysis Report page.
    """
    return service.list_for_analysis(
        analysis_id=analysis_id,
        severity=severity,
    )


@router.post(
    "",
    response_model=AnalysisDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new analysis (paste)",
)
def create_analysis(
    payload: AnalysisCreate,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisDetail:
    """
    Creates a new analysis from pasted text. For file uploads use
    POST /analyses/upload.
    """
    return service.create_analysis(payload)


@router.post(
    "/upload",
    response_model=AnalysisDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new analysis from uploaded document",
)
async def create_analysis_from_upload(
    file: UploadFile = File(..., description="PDF document (max 20 pages)"),
    title: str = Form("", description="Optional title; defaults to filename"),
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisDetail:
    """
    Creates a new analysis from an uploaded PDF. The document must be
    at most 20 pages; otherwise the request is rejected with 400.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are accepted. Please upload a .pdf file.",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File is too large. Maximum size is {settings.UPLOAD_MAX_FILE_SIZE_MB} MB.",
        )

    display_title = (title or "").strip() or (file.filename or "Uploaded document")

    try:
        return service.create_analysis_from_upload(
            file_content=content,
            filename=file.filename or "",
            title=display_title,
            max_pages=settings.UPLOAD_MAX_PAGES,
        )
    except DocumentTooLongError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        ) from e
    except DocumentExtractionError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e

