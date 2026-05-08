from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID as PyUUID

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ApplicationStatus

if TYPE_CHECKING:
    from app.models.ai import AIJob, AIReviewItem
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

    application_number: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )

    student_id: Mapped[PyUUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("student_profiles.id"),
        nullable=False,
    )

    institution_id: Mapped[PyUUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("institutions.id"),
        nullable=True,
    )

    exam_session_id: Mapped[PyUUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("exam_sessions.id"),
        nullable=False,
    )

    subject_id: Mapped[PyUUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        nullable=False,
    )

    grade_level_id: Mapped[PyUUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("grade_levels.id"),
        nullable=True,
    )

    preferred_centre_id: Mapped[PyUUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("exam_centres.id"),
        nullable=True,
    )

    allocated_centre_id: Mapped[PyUUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("exam_centres.id"),
        nullable=True,
    )

    submitted_by_user_id: Mapped[PyUUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    verified_by_user_id: Mapped[PyUUID | None] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(
            ApplicationStatus,
            name="application_status",
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
        default=ApplicationStatus.DRAFT,
        server_default=ApplicationStatus.DRAFT.value,
    )

    fee_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    admin_remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    correction_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    rejected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    student_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    student: Mapped[StudentProfile] = relationship(
        "StudentProfile",
        back_populates="applications",
    )

    institution: Mapped[Institution | None] = relationship(
        "Institution",
        back_populates="applications",
    )

    session: Mapped[ExamSession] = relationship(
        "ExamSession",
        back_populates="applications",
    )

    subject: Mapped[Subject] = relationship(
        "Subject",
        back_populates="applications",
    )

    grade_level: Mapped[GradeLevel | None] = relationship(
        "GradeLevel",
        back_populates="applications",
    )

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
        foreign_keys=[submitted_by_user_id],
        back_populates="submitted_applications",
    )

    verified_by_user: Mapped[User | None] = relationship(
        "User",
        foreign_keys=[verified_by_user_id],
        back_populates="verified_applications",
    )

    payments: Mapped[list[Payment]] = relationship(
        "Payment",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    documents: Mapped[list[Document]] = relationship(
        "Document",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    centre_allocation: Mapped[CentreAllocation | None] = relationship(
        "CentreAllocation",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    admit_card: Mapped[AdmitCard | None] = relationship(
        "AdmitCard",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    marks_entry: Mapped[MarksEntry | None] = relationship(
        "MarksEntry",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    result: Mapped[Result | None] = relationship(
        "Result",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    certificate: Mapped[Certificate | None] = relationship(
        "Certificate",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )

    support_requests: Mapped[list[SupportRequest]] = relationship(
        "SupportRequest",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    ai_jobs: Mapped[list[AIJob]] = relationship(
        "AIJob",
        back_populates="related_application",
        cascade="all, delete-orphan",
    )

    ai_review_items: Mapped[list[AIReviewItem]] = relationship(
        "AIReviewItem",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Application("
            f"id={self.id}, "
            f"application_number={self.application_number!r}, "
            f"status={self.status!r}"
            f")>"
        )