from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import Gender

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.document import Document
    from app.models.user import User


class StudentProfile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "student_profiles"
    __table_args__ = (
        Index("ix_student_profiles_district", "district"),
        Index("ix_student_profiles_pincode", "pincode"),
        Index("ix_student_profiles_guardian_phone", "guardian_phone"),
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[Gender | None] = mapped_column(Enum(Gender, name="gender"), nullable=True)
    guardian_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    guardian_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    guardian_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line_1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line_2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(120), nullable=False, server_default="India")
    photo_document_id: Mapped[UUID | None] = mapped_column(ForeignKey("documents.id"), nullable=True)
    signature_document_id: Mapped[UUID | None] = mapped_column(ForeignKey("documents.id"), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="student_profile", foreign_keys=[user_id])
    applications: Mapped[list[Application]] = relationship("Application", back_populates="student")

    photo_document: Mapped[Document | None] = relationship(
        "Document",
        foreign_keys=[photo_document_id],
        post_update=True,
    )
    signature_document: Mapped[Document | None] = relationship(
        "Document",
        foreign_keys=[signature_document_id],
        post_update=True,
    )
