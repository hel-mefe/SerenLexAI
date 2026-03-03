import uuid
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
from models.base import TimestampMixin


class Clause(Base, TimestampMixin):
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

    clause_type: Mapped[str | None] = mapped_column(String(50))
    position_index: Mapped[int | None] = mapped_column(Integer)

    analysis = relationship("Analysis", back_populates="clauses")