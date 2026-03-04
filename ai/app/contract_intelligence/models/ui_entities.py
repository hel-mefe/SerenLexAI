"""
UI / CRUD entities used as the source of truth for the frontend.

These tables (analyses, clauses, actions) are the workflow output and drive
all UI operations. Action rows implement event-sourcing for user activity.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.contract_intelligence.models.db import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class User(Base, TimestampMixin):
    """
    Minimal user table for FK resolution.

    MVP uses a single logical user and keeps `user_id` nullable, but the `users`
    table still exists in the schema (created by backend migrations). Defining
    it here prevents SQLAlchemy from failing mapper configuration when it sees
    ForeignKey("users.id") on `analyses` / `actions`.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Analysis(Base, TimestampMixin):
    """One analysis run; summary and counts for the UI."""

    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[Optional[str]] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")

    overall_risk: Mapped[Optional[str]] = mapped_column(String(20))
    risk_score: Mapped[Optional[int]] = mapped_column(Integer)

    flagged_count: Mapped[int] = mapped_column(Integer, default=0)
    high_count: Mapped[int] = mapped_column(Integer, default=0)
    medium_count: Mapped[int] = mapped_column(Integer, default=0)
    low_count: Mapped[int] = mapped_column(Integer, default=0)

    raw_text: Mapped[Optional[str]] = mapped_column(Text)

    clauses: Mapped[list["Clause"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )
    actions: Mapped[list["Action"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )


class Clause(Base, TimestampMixin):
    """One clause result; severity and recommendation for the UI."""

    __tablename__ = "clauses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    risk_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)

    clause_type: Mapped[Optional[str]] = mapped_column(String(50))
    position_index: Mapped[Optional[int]] = mapped_column(Integer)

    analysis: Mapped[Analysis] = relationship(back_populates="clauses")


class Action(Base, TimestampMixin):
    """
    Domain event for activity (event-sourcing).
    E.g. document uploaded, processing done, processing failed.
    """

    __tablename__ = "actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    analysis_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    analysis: Mapped[Optional[Analysis]] = relationship(back_populates="actions")
