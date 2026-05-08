from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ApplicationStatus

if TYPE_CHECKING:
    from app.models.centre import AdmitCard, CentreAllocation, ExamCentre
    from app.models.certificate import Certificate
    from app.models.document import Document
    from app.models.exam import ExamSession, GradeLevel, Subject
    from app.models.institution import Institution
    from app.models.payment import Payment
    from app.models.result import MarksEntry, Result
    from app.models.student import StudentProfile
    from app.models.support import SupportRequest
    from app.models.user import User
    from app.models.ai import AIJob, AIReviewItem


class Application(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "applications"
    __table_args__ = (
        Index("ix_applications_application_number", "application_number"),
        Index("ix_applications_status", "status"),
        Index("ix_applications_student_id", "student_id"),
        Index("ix_applications_institution_id", "institution_id"),
        Index("ix_applications_exam_session_id", "exam_session_id"),
        Index("ix_applications_subject_id", "subject_id"),
        Index("ix_applications_allocated_centre_id", "allocated_centre_id"),
    )

    application_number: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("student_profiles.id"), nullable=False)
    institution_id: Mapped[UUID | None] = mapped_column(ForeignKey("institutions.id"), nullable=True)
    exam_session_id: Mapped[UUID] = mapped_column(ForeignKey("exam_sessions.id"), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    grade_level_id: Mapped[UUID | None] = mapped_column(ForeignKey("grade_levels.id"), nullable=True)
    preferred_centre_id: Mapped[UUID | None] = mapped_column(ForeignKey("exam_centres.id"), nullable=True)
    allocated_centre_id: Mapped[UUID | None] = mapped_column(ForeignKey("exam_centres.id"), nullable=True)
    submitted_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    verified_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"),
        nullable=False,
        server_default=ApplicationStatus.DRAFT.value,
    )
    fee_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    admin_remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    correction_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    student: Mapped[StudentProfile] = relationship("StudentProfile", back_populates="applications")
    institution: Mapped[Institution | None] = relationship("Institution", back_populates="applications")
    session: Mapped[ExamSession] = relationship("ExamSession", back_populates="applications")
    subject: Mapped[Subject] = relationship("Subject", back_populates="applications")
    grade_level: Mapped[GradeLevel | None] = relationship("GradeLevel", back_populates="applications")

    preferred_centre: Mapped[ExamCentre | None] = relationship(
        "ExamCentre",
        foreign_keys=[preferred_centre_id],
        back_populates="preferred_applications",
    )
    allocated_centre: Mapped[ExamCentre | None] = relationship(
        "ExamCentre",
        foreign_keys=[allocated_centre_id],
        back_populates="allocated_applications",
    )

    submitted_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="submitted_applications",
        foreign_keys=[submitted_by_user_id],
    )
    verified_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="verified_applications",
        foreign_keys=[verified_by_user_id],
    )

    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="application")
    documents: Mapped[list[Document]] = relationship("Document", back_populates="application")
    centre_allocation: Mapped[CentreAllocation | None] = relationship(
        "CentreAllocation",
        back_populates="application",
        uselist=False,
    )
    admit_card: Mapped[AdmitCard | None] = relationship("AdmitCard", back_populates="application", uselist=False)
    marks_entry: Mapped[MarksEntry | None] = relationship("MarksEntry", back_populates="application", uselist=False)
    result: Mapped[Result | None] = relationship("Result", back_populates="application", uselist=False)
    certificate: Mapped[Certificate | None] = relationship(
        "Certificate",
        back_populates="application",
        uselist=False,
    )
    support_requests: Mapped[list[SupportRequest]] = relationship("SupportRequest", back_populates="application")

    ai_jobs: Mapped[list[AIJob]] = relationship("AIJob", back_populates="related_application")
    ai_review_items: Mapped[list[AIReviewItem]] = relationship("AIReviewItem", back_populates="application")
