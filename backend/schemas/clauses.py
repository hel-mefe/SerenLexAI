from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel

from .analysis import SeverityLevel


class ClauseBase(BaseModel):
    title: str
    severity: SeverityLevel
    original_text: str
    risk_explanation: str
    recommended_action: str
    clause_type: Optional[str] = None
    position_index: Optional[int] = None


class ClauseCreate(ClauseBase):
    analysis_id: uuid.UUID


class ClauseRead(ClauseBase):
    id: uuid.UUID


class ClauseListResponse(BaseModel):
    items: list[ClauseRead]
    total: int

