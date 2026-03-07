from __future__ import annotations

from typing import Optional

from celery import Celery

from core.config import settings
from models.analysis import Analysis


celery_app = Celery(
    "backend_producer",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# langgraph-ai worker consumes this task name
TASK_NAME = "contract_ai.run_analysis"


def enqueue_contract_analysis(
    analysis: Analysis,
    pdf_path: Optional[str] = None,
) -> None:
    """
    Enqueue an analysis job for the langgraph-ai worker (contract_ai).

    The worker expects analysis_id and pdf_path. Only enqueue when we have
    a PDF path (i.e. from upload). Paste analyses are not yet supported.
    """
    if not pdf_path:
        return

    payload = {
        "analysis_id": str(analysis.id),
        "pdf_path": pdf_path,
    }

    celery_app.send_task(TASK_NAME, kwargs={"payload": payload})

