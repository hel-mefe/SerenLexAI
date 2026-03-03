from __future__ import annotations

from sqlalchemy.orm import Session

from repositories.analysis_repository import AnalysisRepository
from repositories.clause_repository import ClauseRepository
from repositories.action_repository import ActionRepository
from services.analysis_service import AnalysisService
from services.clause_service import ClauseService
from services.action_service import ActionService


class Registry:
    """
    Simple application-level registry for wiring repositories and services.

    This keeps construction logic in one place and makes it easy to evolve
    toward a more sophisticated DI container later.
    """

    def get_analysis_service(self, db: Session) -> AnalysisService:
        return AnalysisService(
            db=db,
            analysis_repository=AnalysisRepository(db),
            clause_repository=ClauseRepository(db),
            action_repository=ActionRepository(db),
        )

    def get_clause_service(self, db: Session) -> ClauseService:
        return ClauseService(
            db=db,
            clause_repository=ClauseRepository(db),
        )

    def get_action_service(self, db: Session) -> ActionService:
        return ActionService(
            db=db,
            action_repository=ActionRepository(db),
        )


registry = Registry()

