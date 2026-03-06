from __future__ import annotations

import os

from celery import Celery


def create_celery() -> Celery:
  """
  Celery application for the langgraph-ai contract analysis worker.

  - Broker / backend default to the same Redis URL as the SerenLex stack.
  - Uses JSON serialization for safety across language boundaries.
  """
  redis_url = os.getenv("REDIS_URL", "redis://serenlex_redis:6379/0")

  app = Celery("contract_ai", broker=redis_url, backend=redis_url)
  app.conf.task_serializer = "json"
  app.conf.result_serializer = "json"
  app.conf.accept_content = ["json"]

  return app


celery_app = create_celery()

