from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel


HistoryEventType = Literal["UPLOAD", "COMPLETED", "FAILED"]


class ActionCreate(BaseModel):
    type: HistoryEventType
    title: str
    description: str
    analysis_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    metadata: Optional[Dict[str, Any]] = None


class ActionRead(BaseModel):
    id: uuid.UUID
    type: HistoryEventType
    title: str
    description: str
    created_at: datetime
    analysis_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None


class ActionsListResponse(BaseModel):
    items: list[ActionRead]
    total: int

