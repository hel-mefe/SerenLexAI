from __future__ import annotations

from celery import Celery

from core.config import settings
from models.analysis import Analysis


celery_app = Celery(
    "backend_producer",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

TASK_NAME = "contract_intelligence.run_analysis"


def enqueue_contract_analysis(analysis: Analysis) -> None:
    """
    Enqueue an analysis job for the AI worker.

    The AI worker will populate analyses/clauses based on this analysis.
    """
    if not analysis.raw_text:
        # For now we only send text-based jobs; PDF ingestion was already done.
        return

    payload = {
        "contract_id": str(analysis.id),
        "analysis_run_id": str(analysis.id),
        "user_id": None,
        "raw_input": analysis.raw_text,
        "is_base64": False,
        "file_name": analysis.original_filename,
        "content_type": "text/plain",
        "metadata": {
            "source_type": analysis.source_type,
        },
    }

    celery_app.send_task(TASK_NAME, kwargs={"payload": payload})

