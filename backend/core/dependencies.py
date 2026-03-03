from __future__ import annotations

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.registry import registry
from services.analysis_service import AnalysisService
from services.clause_service import ClauseService
from services.action_service import ActionService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_analysis_service(
    db: Session = Depends(get_db),
) -> AnalysisService:
    return registry.get_analysis_service(db)


def get_clause_service(
    db: Session = Depends(get_db),
) -> ClauseService:
    return registry.get_clause_service(db)


def get_action_service(
    db: Session = Depends(get_db),
) -> ActionService:
    return registry.get_action_service(db)

