from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import CentreStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.document import Document
    from app.models.user import User


class ExamCentre(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "exam_centres"
    __table_args__ = (
        Index("ix_exam_centres_code", "code"),
        Index("ix_exam_centres_district", "district"),
        Index("ix_exam_centres_pincode", "pincode"),
        Index("ix_exam_centres_status", "status"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    address_line_1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line_2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_person_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_person_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    status: Mapped[CentreStatus] = mapped_column(
        Enum(CentreStatus, name="centre_status"),
        nullable=False,
        server_default=CentreStatus.ACTIVE.value,
    )
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    preferred_applications: Mapped[list[Application]] = relationship(
        "Application",
        back_populates="preferred_centre",
        foreign_keys="Application.preferred_centre_id",
    )
    allocated_applications: Mapped[list[Application]] = relationship(
        "Application",
        back_populates="allocated_centre",
        foreign_keys="Application.allocated_centre_id",
    )
    centre_allocations: Mapped[list[CentreAllocation]] = relationship("CentreAllocation", back_populates="centre")
    admit_cards: Mapped[list[AdmitCard]] = relationship("AdmitCard", back_populates="centre")


class CentreAllocation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "centre_allocations"
    __table_args__ = (
        Index("ix_centre_allocations_centre_id", "centre_id"),
        Index("ix_centre_allocations_application_id", "application_id"),
    )

    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id"), nullable=False, unique=True)
    centre_id: Mapped[UUID] = mapped_column(ForeignKey("exam_centres.id"), nullable=False)
    allocated_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    allocation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_recommended: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    ai_confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    allocated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    application: Mapped[Application] = relationship("Application", back_populates="centre_allocation")
    centre: Mapped[ExamCentre] = relationship("ExamCentre", back_populates="centre_allocations")
    allocated_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="allocated_centres",
        foreign_keys=[allocated_by_user_id],
    )


class AdmitCard(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "admit_cards"
    __table_args__ = (
        Index("ix_admit_cards_roll_number", "roll_number"),
        Index("ix_admit_cards_qr_code_value", "qr_code_value"),
        Index("ix_admit_cards_centre_id", "centre_id"),
    )

    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id"), nullable=False, unique=True)
    roll_number: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    exam_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reporting_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    exam_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    centre_id: Mapped[UUID | None] = mapped_column(ForeignKey("exam_centres.id"), nullable=True)
    pdf_document_id: Mapped[UUID | None] = mapped_column(ForeignKey("documents.id"), nullable=True)
    qr_code_value: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    verification_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    generated_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    generated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    application: Mapped[Application] = relationship("Application", back_populates="admit_card")
    centre: Mapped[ExamCentre | None] = relationship("ExamCentre", back_populates="admit_cards")
    pdf_document: Mapped[Document | None] = relationship("Document", foreign_keys=[pdf_document_id])
    generated_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="generated_admit_cards",
        foreign_keys=[generated_by_user_id],
    )
