from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import SupportStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class SupportRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "support_requests"
    __table_args__ = (
        Index("ix_support_requests_status", "status"),
        Index("ix_support_requests_user_id", "user_id"),
        Index("ix_support_requests_application_id", "application_id"),
    )

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    application_id: Mapped[UUID | None] = mapped_column(ForeignKey("applications.id"), nullable=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[SupportStatus] = mapped_column(
        Enum(SupportStatus, name="support_status"),
        nullable=False,
        server_default=SupportStatus.OPEN.value,
    )
    assigned_to_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolution_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User | None] = relationship(
        "User",
        back_populates="support_requests",
        foreign_keys=[user_id],
    )
    assigned_to_user: Mapped[User | None] = relationship(
        "User",
        back_populates="assigned_support_requests",
        foreign_keys=[assigned_to_user_id],
    )
    application: Mapped[Application | None] = relationship("Application", back_populates="support_requests")
