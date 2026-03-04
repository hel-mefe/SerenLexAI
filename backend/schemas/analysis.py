from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


SeverityLevel = Literal["High", "Medium", "Low"]
RiskLevel = SeverityLevel


class AnalysisBase(BaseModel):
    title: str
    original_filename: Optional[str] = None
    source_type: str = Field(..., description="e.g. 'upload' or 'paste'")


class AnalysisCreate(AnalysisBase):
    raw_text: Optional[str] = Field(
        None,
        description=(
            "Optional raw text of the contract. "
            "LLM worker can use this later for analysis."
        ),
    )


class AnalysisSummary(BaseModel):
    id: uuid.UUID
    title: str
    analyzed_at: datetime
    flagged_count: int
    score: int
    overall_risk: Optional[RiskLevel] = None
    high: int
    medium: int
    low: int


class AnalysisListItem(BaseModel):
    id: uuid.UUID
    name: str
    date: datetime
    risk: Optional[RiskLevel] = None
    clauses: int
    score: int
    status: str


class AnalysisDetail(BaseModel):
    id: uuid.UUID
    title: str
    original_filename: Optional[str] = None
    source_type: str
    status: str
    overall_risk: Optional[RiskLevel] = None
    risk_score: Optional[int] = None
    flagged_count: int
    high_count: int
    medium_count: int
    low_count: int
    created_at: datetime
    updated_at: datetime


class AnalysisListResponse(BaseModel):
    items: list[AnalysisListItem]
    total: int
    page: int
    page_size: int

