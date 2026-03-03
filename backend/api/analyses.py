from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.dependencies import get_analysis_service, get_clause_service
from schemas.analysis import (
    AnalysisCreate,
    AnalysisDetail,
    AnalysisListResponse,
)
from schemas.clauses import ClauseListResponse
from services.analysis_service import AnalysisService
from services.clause_service import ClauseService


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
    summary="Create a new analysis",
)
def create_analysis(
    payload: AnalysisCreate,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisDetail:
    """
    Creates a new analysis from either uploaded content or pasted text.
    For the MVP, this simply stores metadata and raw_text; the LLM worker
    can later populate risk metrics and clauses based on this record.
    """
    return service.create_analysis(payload)

