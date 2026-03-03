from __future__ import annotations

from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.clauses import Clause


class ClauseRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_by_analysis(
        self,
        analysis_id,
        *,
        severity: Optional[str] = None,
    ) -> Tuple[List[Clause], int]:
        query = select(Clause).where(Clause.analysis_id == analysis_id)

        if severity:
            query = query.where(Clause.severity == severity)

        query = query.order_by(Clause.position_index.asc())
        items = list(self._db.scalars(query).all())
        return items, len(items)

