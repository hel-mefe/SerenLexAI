from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


RiskLevel = Literal["low", "medium", "high", "critical"]


class AnalyzeFileMetadata(BaseModel):
    contract_value: Optional[float] = None
    currency: Optional[str] = None
    extra: dict[str, Any] = Field(default_factory=dict)


class AnalyzeTextRequest(BaseModel):
    title: Optional[str] = None
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClauseResponse(BaseModel):
    clause_type: str
    section_type: Optional[str]
    extracted_text: str
    risk_level: Optional[RiskLevel]
    risk_score: Optional[float]
    risk_rationale: Optional[str]
    recommendation: Optional[str]
    suggested_language: Optional[str]
    page_start: Optional[int]
    page_end: Optional[int]


class ScoreBreakdown(BaseModel):
    by_section: dict[str, float] = Field(default_factory=dict)
    top_risks: list[dict[str, Any]] = Field(default_factory=list)
    clause_count: int = 0
    high_risk_count: int = 0
    critical_risk_count: int = 0


class AnalysisExecutionSummary(BaseModel):
    total_latency_ms: Optional[int] = None
    nodes_completed: int
    total_tokens: Optional[int] = None
    workflow_version: str


class AnalyzeResponse(BaseModel):
    contract_id: str
    analysis_run_id: str
    status: Literal["pending", "running", "completed", "failed", "partial"]
    risk_score: Optional[float]
    risk_level: Optional[RiskLevel]
    score_breakdown: Optional[ScoreBreakdown]
    clauses: list[ClauseResponse]
    explanation: Optional[str]
    errors: list[dict[str, Any]]
    execution_summary: AnalysisExecutionSummary


class AnalysisRunSummary(BaseModel):
    id: str
    status: str
    overall_risk_score: Optional[float]
    overall_risk_level: Optional[str]
    clause_count: Optional[int]
    high_risk_count: Optional[int]
    critical_risk_count: Optional[int]
    started_at: datetime
    completed_at: Optional[datetime]


class NodeExecutionTrace(BaseModel):
    id: str
    analysis_run_id: str
    node_name: str
    status: str
    input_snapshot: Optional[dict[str, Any]]
    output_snapshot: Optional[dict[str, Any]]
    tool_calls: list[dict[str, Any]]
    model_used: Optional[str]
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    latency_ms: Optional[int]
    error: Optional[str]
    executed_at: datetime

