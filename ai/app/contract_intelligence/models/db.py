from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, VECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    normalized_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    input_format: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    sections: Mapped[list["ContractSection"]] = relationship(
        back_populates="contract",
        cascade="all, delete-orphan",
    )
    analysis_runs: Mapped[list["AnalysisRun"]] = relationship(
        back_populates="contract",
        cascade="all, delete-orphan",
    )


class ContractSection(Base):
    __tablename__ = "contract_sections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_type: Mapped[str] = mapped_column(Text, nullable=False)
    clause_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    page_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    page_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    position_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    embedding: Mapped[Optional[list[float]]] = mapped_column(
        VECTOR(1536),
        nullable=True,
    )
    is_amendment: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    contract: Mapped[Contract] = relationship(back_populates="sections")
    clause_results: Mapped[list["ClauseResult"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
    )


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String,
        default="pending",
    )
    overall_risk_score: Mapped[Optional[float]] = mapped_column(
        Numeric(4, 2), nullable=True
    )
    overall_risk_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    score_breakdown: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    clause_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    high_risk_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    critical_risk_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    workflow_version: Mapped[str] = mapped_column(String, default="1.0.0")
    total_tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_summary: Mapped[list[Any]] = mapped_column(JSON, default=list)

    contract: Mapped[Contract] = relationship(back_populates="analysis_runs")
    clause_results: Mapped[list["ClauseResult"]] = relationship(
        back_populates="analysis_run",
        cascade="all, delete-orphan",
    )
    node_executions: Mapped[list["NodeExecution"]] = relationship(
        back_populates="analysis_run",
        cascade="all, delete-orphan",
    )


class ClauseResult(Base):
    __tablename__ = "clause_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("contract_sections.id", ondelete="CASCADE"),
        nullable=True,
    )
    clause_type: Mapped[str] = mapped_column(Text, nullable=False)
    section_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)
    key_terms: Mapped[list[Any]] = mapped_column(JSON, default=list)
    defined_terms_used: Mapped[list[Any]] = mapped_column(JSON, default=list)
    cross_references: Mapped[list[Any]] = mapped_column(JSON, default=list)
    risk_level: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    risk_score: Mapped[Optional[float]] = mapped_column(Numeric(4, 2), nullable=True)
    risk_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suggested_language: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendation_priority: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    similar_precedents: Mapped[list[Any]] = mapped_column(JSON, default=list)
    page_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    page_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    section: Mapped[Optional[ContractSection]] = relationship(
        back_populates="clause_results"
    )
    analysis_run: Mapped[AnalysisRun] = relationship(back_populates="clause_results")


class NodeExecution(Base):
    __tablename__ = "node_executions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    node_name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    input_snapshot: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    output_snapshot: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    tool_calls: Mapped[list[Any]] = mapped_column(JSON, default=list)
    model_used: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    analysis_run: Mapped[AnalysisRun] = relationship(back_populates="node_executions")

