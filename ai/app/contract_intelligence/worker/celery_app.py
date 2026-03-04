from __future__ import annotations

from celery import Celery

from app.contract_intelligence.config import get_settings


def create_celery() -> Celery:
    settings = get_settings()
    app = Celery("contract_intelligence", broker=settings.redis_url, backend=settings.redis_url)
    app.conf.task_serializer = "json"
    app.conf.result_serializer = "json"
    app.conf.accept_content = ["json"]
    return app


celery_app = create_celery()

