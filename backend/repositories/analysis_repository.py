from __future__ import annotations

from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.clauses import Clause


class AnalysisRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, analysis_id) -> Optional[Analysis]:
        return self._db.get(Analysis, analysis_id)

    def list_paginated(
        self,
        *,
        search: Optional[str],
        risk: Optional[str],
        page: int,
        page_size: int,
    ) -> Tuple[List[Analysis], int]:
        query = select(Analysis)

        if search:
            ilike = f"%{search.lower()}%"
            query = query.where(func.lower(Analysis.title).like(ilike))

        if risk:
            query = query.where(Analysis.overall_risk == risk)

        total = self._db.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = (
            query.order_by(Analysis.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = list(self._db.scalars(query).all())
        return items, int(total or 0)

    def create(self, analysis: Analysis) -> Analysis:
        self._db.add(analysis)
        self._db.flush()
        self._db.refresh(analysis)
        return analysis

    def count_clauses(self, analysis_id) -> int:
        stmt = (
            select(func.count(Clause.id))
            .where(Clause.analysis_id == analysis_id)
        )
        count = self._db.scalar(stmt)
        return int(count or 0)

