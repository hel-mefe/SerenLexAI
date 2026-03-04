from __future__ import annotations

from typing import Any, Literal, Optional, List

from pydantic import BaseModel, Field

from app.contract_intelligence.models.domain import (
    BlockModel,
    ChunkModel,
    ClassifiedClauseModel,
    NodeErrorModel,
    RecommendationModel,
    SectionModel,
)


class ContractState(BaseModel):
    contract_id: str
    analysis_run_id: str
    raw_input: str | bytes
    input_format: Literal["pdf", "docx", "text"]
    extracted_blocks: List[BlockModel] = Field(default_factory=list)
    chunks: List[ChunkModel] = Field(default_factory=list)
    normalized_chunks: List[ChunkModel] = Field(default_factory=list)
    sections: List[SectionModel] = Field(default_factory=list)
    clauses: List[ClassifiedClauseModel] = Field(default_factory=list)
    classified_clauses: List[ClassifiedClauseModel] = Field(default_factory=list)
    risk_score: float = 0.0
    risk_level: Literal["low", "medium", "high", "critical"] = "low"
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    recommendations: List[RecommendationModel] = Field(default_factory=list)
    explanation: str = ""
    node_executions: List[dict[str, Any]] = Field(default_factory=list)
    errors: List[NodeErrorModel] = Field(default_factory=list)
    fatal_error: Optional[str] = None
    page_count: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)
    total_latency_ms: int = 0
    total_tokens_used: int = 0
    analysis_id: Optional[str] = None
    user_id: Optional[str] = None

