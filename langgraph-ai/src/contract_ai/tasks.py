from __future__ import annotations

import uuid
from typing import Any, Dict

from .application.workflows.contract_analysis_graph import build_graph
from .celery_app import celery_app
from .domain.exceptions import DocumentTooLongError
from .infrastructure.db import SessionLocal
from .infrastructure.models import Analysis


def _mark_analysis_failed(analysis_id: str, reason: str = "Analysis failed.") -> None:
    """Update the analysis row to status='failed' so the UI can show failure."""
    db = SessionLocal()
    try:
        aid = uuid.UUID(analysis_id)
        row = db.get(Analysis, aid)
        if row:
            row.status = "failed"
            db.commit()
    except (TypeError, ValueError):
        pass
    finally:
        db.close()


@celery_app.task(name="contract_ai.run_analysis")
def run_analysis_task(payload: Dict[str, Any]) -> None:
  """
  Celery task entrypoint for running the langgraph-based contract analysis.

  Expected payload structure:
  - analysis_id: UUID (as string) of the analysis row in the SerenLex DB.
  - pdf_path: absolute or container-local path to the PDF to analyse,
    OR an object storage key/URL (e.g. MinIO) if your graph knows how to fetch it.

  Rejects PDFs with more than 20 pages (validated in the graph); marks the
  analysis as 'failed' in the DB when that happens so the backend/UI can show it.
  """
  analysis_id = str(payload.get("analysis_id") or uuid.uuid4())
  pdf_path = payload.get("pdf_path")

  if not pdf_path:
    raise ValueError("run_analysis_task: 'pdf_path' is required in payload")

  graph = build_graph()
  state: Dict[str, Any] = {
    "analysis_id": analysis_id,
    "pdf_path": pdf_path,
  }

  try:
    graph.invoke(state)
  except DocumentTooLongError as e:
    _mark_analysis_failed(analysis_id, str(e))
    raise

