from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class AnalysisTaskPayload(BaseModel):
    """Payload for the analysis Celery task; must match what producers send."""

    contract_id: Optional[str] = None
    analysis_run_id: Optional[str] = None
    user_id: Optional[str] = None
    raw_input: str
    is_base64: bool = False
    file_name: Optional[str] = None
    content_type: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

