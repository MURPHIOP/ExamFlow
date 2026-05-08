from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AIJobStatus, AIJobType, AIReviewStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class AIJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "ai_jobs"
    __table_args__ = (
        Index("ix_ai_jobs_job_type", "job_type"),
        Index("ix_ai_jobs_status", "status"),
        Index("ix_ai_jobs_related_application_id", "related_application_id"),
        Index("ix_ai_jobs_created_at", "created_at"),
    )

    job_type: Mapped[AIJobType] = mapped_column(Enum(AIJobType, name="ai_job_type"), nullable=False)
    status: Mapped[AIJobStatus] = mapped_column(
        Enum(AIJobStatus, name="ai_job_status"),
        nullable=False,
        server_default=AIJobStatus.QUEUED.value,
    )
    related_application_id: Mapped[UUID | None] = mapped_column(ForeignKey("applications.id"), nullable=True)
    related_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    input_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    output_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    related_application: Mapped[Application | None] = relationship("Application", back_populates="ai_jobs")
    related_user: Mapped[User | None] = relationship(
        "User",
        back_populates="related_ai_jobs",
        foreign_keys=[related_user_id],
    )
    created_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="created_ai_jobs",
        foreign_keys=[created_by_user_id],
    )
    review_items: Mapped[list[AIReviewItem]] = relationship("AIReviewItem", back_populates="ai_job")


class AIReviewItem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "ai_review_items"
    __table_args__ = (
        Index("ix_ai_review_items_ai_job_id", "ai_job_id"),
        Index("ix_ai_review_items_application_id", "application_id"),
        Index("ix_ai_review_items_status", "status"),
        Index("ix_ai_review_items_review_type", "review_type"),
    )

    ai_job_id: Mapped[UUID] = mapped_column(ForeignKey("ai_jobs.id"), nullable=False)
    application_id: Mapped[UUID | None] = mapped_column(ForeignKey("applications.id"), nullable=True)
    review_type: Mapped[str] = mapped_column(String(120), nullable=False)
    suggestion_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[AIReviewStatus] = mapped_column(
        Enum(AIReviewStatus, name="ai_review_status"),
        nullable=False,
        server_default=AIReviewStatus.PENDING_REVIEW.value,
    )
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    admin_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    ai_job: Mapped[AIJob] = relationship("AIJob", back_populates="review_items")
    application: Mapped[Application | None] = relationship("Application", back_populates="ai_review_items")
    reviewed_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="reviewed_ai_items",
        foreign_keys=[reviewed_by_user_id],
    )
