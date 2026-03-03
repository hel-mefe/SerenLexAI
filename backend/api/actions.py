from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from core.dependencies import get_action_service
from schemas.actions import ActionsListResponse
from services.action_service import ActionService


router = APIRouter(prefix="/actions", tags=["actions"])


@router.get(
    "",
    response_model=ActionsListResponse,
    summary="List actions (event history)",
)
def list_actions(
    type: Optional[str] = Query(
        default=None,
        description="Optional filter on event type (UPLOAD, COMPLETED, FAILED)",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ActionService = Depends(get_action_service),
) -> ActionsListResponse:
    """
    Returns a paginated stream of actions, which can power the dashboard
    history timeline and per-analysis activity feeds.
    """
    return service.list_actions(
        type=type,
        page=page,
        page_size=page_size,
    )

