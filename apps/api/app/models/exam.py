from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ExamSessionStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class ExamSession(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "exam_sessions"
    __table_args__ = (
        Index("ix_exam_sessions_code", "code"),
        Index("ix_exam_sessions_year", "year"),
        Index("ix_exam_sessions_status", "status"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    application_start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    application_end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    exam_start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    exam_end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result_publish_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    certificate_issue_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[ExamSessionStatus] = mapped_column(
        Enum(ExamSessionStatus, name="exam_session_status"),
        nullable=False,
        server_default=ExamSessionStatus.DRAFT.value,
    )
    created_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    created_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="created_exam_sessions",
        foreign_keys=[created_by_user_id],
    )
    applications: Mapped[list[Application]] = relationship("Application", back_populates="session")
    exam_fees: Mapped[list[ExamFee]] = relationship("ExamFee", back_populates="exam_session")


class Subject(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "subjects"
    __table_args__ = (
        Index("ix_subjects_name", "name"),
        Index("ix_subjects_code", "code"),
        Index("ix_subjects_category", "category"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    category: Mapped[str | None] = mapped_column(String(120), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default="true")

    grade_levels: Mapped[list[GradeLevel]] = relationship("GradeLevel", back_populates="subject")
    exam_fees: Mapped[list[ExamFee]] = relationship("ExamFee", back_populates="subject")
    applications: Mapped[list[Application]] = relationship("Application", back_populates="subject")


class GradeLevel(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "grade_levels"
    __table_args__ = (UniqueConstraint("subject_id", "code", name="uq_grade_levels_subject_code"),)

    subject_id: Mapped[UUID | None] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    default_fee: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default="true")

    subject: Mapped[Subject | None] = relationship("Subject", back_populates="grade_levels")
    exam_fees: Mapped[list[ExamFee]] = relationship("ExamFee", back_populates="grade_level")
    applications: Mapped[list[Application]] = relationship("Application", back_populates="grade_level")


class ExamFee(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "exam_fees"
    __table_args__ = (
        UniqueConstraint(
            "exam_session_id",
            "subject_id",
            "grade_level_id",
            name="uq_exam_fees_session_subject_grade",
        ),
    )

    exam_session_id: Mapped[UUID] = mapped_column(ForeignKey("exam_sessions.id"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    grade_level_id: Mapped[UUID | None] = mapped_column(ForeignKey("grade_levels.id"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, server_default="INR")
    late_fee_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="0")
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default="true")

    exam_session: Mapped[ExamSession] = relationship("ExamSession", back_populates="exam_fees")
    subject: Mapped[Subject] = relationship("Subject", back_populates="exam_fees")
    grade_level: Mapped[GradeLevel | None] = relationship("GradeLevel", back_populates="exam_fees")
