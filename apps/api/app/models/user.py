from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.ai import AIJob, AIReviewItem
    from app.models.application import Application
    from app.models.audit import AuditLog
    from app.models.centre import AdmitCard, CentreAllocation
    from app.models.document import Document
    from app.models.exam import ExamSession
    from app.models.institution import Institution
    from app.models.notification import Notification
    from app.models.payment import Payment
    from app.models.result import MarksEntry, Result
    from app.models.student import StudentProfile
    from app.models.support import SupportRequest


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_role", "role"),
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_phone", "phone", unique=True),
    )

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    student_profile: Mapped[StudentProfile | None] = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        foreign_keys="StudentProfile.user_id",
    )
    institution_profile: Mapped[Institution | None] = relationship(
        "Institution",
        back_populates="user",
        uselist=False,
        foreign_keys="Institution.user_id",
    )

    submitted_applications: Mapped[list[Application]] = relationship(
        "Application",
        back_populates="submitted_by_user",
        foreign_keys="Application.submitted_by_user_id",
    )
    verified_applications: Mapped[list[Application]] = relationship(
        "Application",
        back_populates="verified_by_user",
        foreign_keys="Application.verified_by_user_id",
    )

    approved_institutions: Mapped[list[Institution]] = relationship(
        "Institution",
        back_populates="approved_by_user",
        foreign_keys="Institution.approved_by_user_id",
    )

    created_exam_sessions: Mapped[list[ExamSession]] = relationship(
        "ExamSession",
        back_populates="created_by_user",
        foreign_keys="ExamSession.created_by_user_id",
    )

    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="user")

    owned_documents: Mapped[list[Document]] = relationship(
        "Document",
        back_populates="owner_user",
        foreign_keys="Document.owner_user_id",
    )
    verified_documents: Mapped[list[Document]] = relationship(
        "Document",
        back_populates="verified_by_user",
        foreign_keys="Document.verified_by_user_id",
    )

    allocated_centres: Mapped[list[CentreAllocation]] = relationship(
        "CentreAllocation",
        back_populates="allocated_by_user",
        foreign_keys="CentreAllocation.allocated_by_user_id",
    )

    generated_admit_cards: Mapped[list[AdmitCard]] = relationship(
        "AdmitCard",
        back_populates="generated_by_user",
        foreign_keys="AdmitCard.generated_by_user_id",
    )

    entered_marks: Mapped[list[MarksEntry]] = relationship(
        "MarksEntry",
        back_populates="entered_by_user",
        foreign_keys="MarksEntry.entered_by_user_id",
    )
    published_results: Mapped[list[Result]] = relationship(
        "Result",
        back_populates="published_by_user",
        foreign_keys="Result.published_by_user_id",
    )

    notifications: Mapped[list[Notification]] = relationship("Notification", back_populates="user")

    support_requests: Mapped[list[SupportRequest]] = relationship(
        "SupportRequest",
        back_populates="user",
        foreign_keys="SupportRequest.user_id",
    )
    assigned_support_requests: Mapped[list[SupportRequest]] = relationship(
        "SupportRequest",
        back_populates="assigned_to_user",
        foreign_keys="SupportRequest.assigned_to_user_id",
    )

    audit_logs: Mapped[list[AuditLog]] = relationship("AuditLog", back_populates="actor_user")

    created_ai_jobs: Mapped[list[AIJob]] = relationship(
        "AIJob",
        back_populates="created_by_user",
        foreign_keys="AIJob.created_by_user_id",
    )
    related_ai_jobs: Mapped[list[AIJob]] = relationship(
        "AIJob",
        back_populates="related_user",
        foreign_keys="AIJob.related_user_id",
    )
    reviewed_ai_items: Mapped[list[AIReviewItem]] = relationship(
        "AIReviewItem",
        back_populates="reviewed_by_user",
        foreign_keys="AIReviewItem.reviewed_by_user_id",
    )
