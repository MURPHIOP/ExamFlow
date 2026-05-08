from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import InstitutionStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class Institution(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "institutions"
    __table_args__ = (
        Index("ix_institutions_institution_name", "institution_name"),
        Index("ix_institutions_district", "district"),
        Index("ix_institutions_status", "status"),
    )

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True, unique=True)
    institution_name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_number: Mapped[str | None] = mapped_column(String(120), nullable=True, unique=True)
    contact_person_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_person_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_person_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line_1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line_2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(120), nullable=False, server_default="India")
    status: Mapped[InstitutionStatus] = mapped_column(
        Enum(InstitutionStatus, name="institution_status"),
        nullable=False,
        server_default=InstitutionStatus.PENDING.value,
    )
    approved_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User | None] = relationship(
        "User",
        back_populates="institution_profile",
        foreign_keys=[user_id],
    )
    approved_by_user: Mapped[User | None] = relationship(
        "User",
        back_populates="approved_institutions",
        foreign_keys=[approved_by_user_id],
    )
    applications: Mapped[list[Application]] = relationship("Application", back_populates="institution")
