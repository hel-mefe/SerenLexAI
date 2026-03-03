from __future__ import annotations

from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.actions import Action


class ActionRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def log(self, action: Action) -> Action:
        self._db.add(action)
        self._db.flush()
        self._db.refresh(action)
        return action

    def list_recent(
        self,
        *,
        limit: int = 20,
        type: Optional[str] = None,
        analysis_id: Optional[str] = None,
    ) -> List[Action]:
        query = select(Action)

        if type:
            query = query.where(Action.type == type)

        if analysis_id:
            query = query.where(Action.analysis_id == analysis_id)

        query = query.order_by(Action.created_at.desc()).limit(limit)
        return list(self._db.scalars(query).all())

    def list_paginated(
        self,
        *,
        type: Optional[str],
        page: int,
        page_size: int,
    ) -> Tuple[List[Action], int]:
        query = select(Action)

        if type:
            query = query.where(Action.type == type)

        total = len(self._db.scalars(query).all())

        query = (
            query.order_by(Action.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = list(self._db.scalars(query).all())
        return items, total

