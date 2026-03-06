from __future__ import annotations

import uuid
from typing import Any, Dict

from .application.workflows.contract_analysis_graph import build_graph
from .celery_app import celery_app


@celery_app.task(name="contract_ai.run_analysis")
def run_analysis_task(payload: Dict[str, Any]) -> None:
  """
  Celery task entrypoint for running the langgraph-based contract analysis.

  Expected payload structure:
  - analysis_id: UUID (as string) of the analysis row in the SerenLex DB.
  - pdf_path: absolute or container-local path to the PDF to analyse,
    OR an object storage key/URL (e.g. MinIO) if your graph knows how to fetch it.

  This function delegates all heavy lifting to the LangGraph workflow
  defined in `contract_analysis_graph.build_graph()`. The graph is
  responsible for:
  - reading the PDF (from pdf_path),
  - running the document / clause / risk analysis,
  - persisting results via its own persistence nodes.
  """
  analysis_id = str(payload.get("analysis_id") or uuid.uuid4())
  pdf_path = payload.get("pdf_path")

  if not pdf_path:
    # Nothing to do without a document location; fail fast.
    # Celery will record this as a task failure in the result backend.
    raise ValueError("run_analysis_task: 'pdf_path' is required in payload")

  graph = build_graph()

  state: Dict[str, Any] = {
    "analysis_id": analysis_id,
    "pdf_path": pdf_path,
  }

  # Fire the full graph; any persistence/reporting is handled by its nodes.
  graph.invoke(state)

