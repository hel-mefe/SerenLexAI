from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class BlockModel(BaseModel):
    text: str
    font_size: Optional[float] = None
    is_bold: bool = False
    page_number: int = 1
    block_type_hint: Optional[str] = None


class ChunkModel(BaseModel):
    id: str
    contract_id: str
    clause_number: Optional[str] = None
    section_type_hint: Optional[str] = None
    content: str
    page_start: int
    page_end: int
    char_count: int
    token_count_estimate: int
    chunk_index: int
    is_schedule: bool = False
    has_annotation: bool = False


class SectionModel(ChunkModel):
    section_type: str = "other"


class ClauseBaseModel(BaseModel):
    clause_type: str
    extracted_text: str
    key_terms: List[str] = Field(default_factory=list)
    defined_terms_used: List[str] = Field(default_factory=list)
    cross_references: List[str] = Field(default_factory=list)
    is_amendment: bool = False
    original_text_if_amended: str = ""
    chunk_id: str
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    section_type: Optional[str] = None


class ClassifiedClauseModel(ClauseBaseModel):
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    risk_rationale: Optional[str] = None
    similar_precedents: List[dict[str, Any]] = Field(default_factory=list)


class RecommendationModel(BaseModel):
    clause_ref: str
    recommendation_text: str
    suggested_language: str
    priority: str
    clause_type: Optional[str] = None
    section_type: Optional[str] = None


class NodeErrorModel(BaseModel):
    node: str
    clause_id: Optional[str] = None
    error_type: str
    message: str

