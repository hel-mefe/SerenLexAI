from __future__ import annotations

from app.contract_intelligence.models.tasks import AnalysisTaskPayload
from app.contract_intelligence.worker.celery_app import celery_app
from app.contract_intelligence.worker.service import AnalysisWorker


@celery_app.task(name="contract_intelligence.run_analysis")
def run_analysis_task(payload: dict) -> None:
    data = AnalysisTaskPayload(**payload)
    worker = AnalysisWorker()
    import asyncio

    asyncio.run(worker.run(data))

