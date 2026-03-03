from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from repositories.action_repository import ActionRepository
from schemas.actions import ActionsListResponse, ActionRead


class ActionService:
    def __init__(
        self,
        db: Session,
        action_repository: ActionRepository,
    ) -> None:
        self._db = db
        self._actions = action_repository

    def list_actions(
        self,
        *,
        type: Optional[str],
        page: int,
        page_size: int,
    ) -> ActionsListResponse:
        items, total = self._actions.list_paginated(
            type=type,
            page=page,
            page_size=page_size,
        )

        return ActionsListResponse(
            items=[
                ActionRead(
                    id=a.id,
                    type=a.type,  # type: ignore[arg-type]
                    title=a.title,
                    description=a.description,
                    created_at=a.created_at,
                    analysis_id=a.analysis_id,
                    user_id=a.user_id,
                )
                for a in items
            ],
            total=total,
        )

