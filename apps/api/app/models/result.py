from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ResultStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class MarksEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "marks_entries"
    __table_args__ = (
        Index("ix_marks_entries_application_id", "application_id"),
        Index("ix_marks_entries_entered_by_user_id", "entered_by_user_id"),
        Index("ix_marks_entries_grade", "grade"),
    )

    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id"), nullable=False, unique=True)
    entered_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    theory_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    practical_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    viva_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    internal_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    total_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    maximum_marks: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="100")
    percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_absent: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    entered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    application: Mapped[Application] = relationship("Application", back_populates="marks_entry")
    entered_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="entered_marks",
        foreign_keys=[entered_by_user_id],
    )
    result: Mapped[Result | None] = relationship("Result", back_populates="marks_entry", uselist=False)


class Result(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "results"
    __table_args__ = (
        Index("ix_results_application_id", "application_id"),
        Index("ix_results_status", "status"),
        Index("ix_results_grade", "grade"),
        Index("ix_results_published_at", "published_at"),
    )

    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id"), nullable=False, unique=True)
    marks_entry_id: Mapped[UUID | None] = mapped_column(ForeignKey("marks_entries.id"), nullable=True, unique=True)
    status: Mapped[ResultStatus] = mapped_column(
        Enum(ResultStatus, name="result_status"),
        nullable=False,
        server_default=ResultStatus.DRAFT.value,
    )
    result_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    total_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    published_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    withheld_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    application: Mapped[Application] = relationship("Application", back_populates="result")
    marks_entry: Mapped[MarksEntry | None] = relationship("MarksEntry", back_populates="result")
    published_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="published_results",
        foreign_keys=[published_by_user_id],
    )
