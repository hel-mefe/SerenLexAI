import uuid
from typing import Any, Dict, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.base import TimestampMixin


class Action(Base, TimestampMixin):
    """
    Domain event representing something that happened in the system.

    This is intentionally generic so we can support both:
    - analysis-centric events (UPLOAD, COMPLETED, FAILED, etc.)
    - user-centric events later when authentication is added.
    """

    __tablename__ = "actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Optional association to a user (MVP may leave this null)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    # Optional association to a specific analysis
    analysis_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # High-level event type, aligned with frontend HistoryEventType for now
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Short human-readable label, e.g. "Contract Uploaded"
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Longer description, e.g. "Service Agreement — Acme Corp"
    description: Mapped[str] = mapped_column(String(512), nullable=False)

    # Free-form structured data for analytics / future features
    # Use attribute name `meta` to avoid clashing with SQLAlchemy's reserved `metadata`.
    meta: Mapped[Dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    analysis = relationship("Analysis", back_populates="actions")
    user = relationship("User", back_populates="actions")

