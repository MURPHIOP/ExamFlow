from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PaymentProvider, PaymentStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.user import User


class Payment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payments_application_id", "application_id"),
        Index("ix_payments_provider_order_id", "provider_order_id", unique=True),
        Index("ix_payments_provider_payment_id", "provider_payment_id", unique=True),
        Index("ix_payments_receipt_number", "receipt_number", unique=True),
        Index("ix_payments_status", "status"),
    )

    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id"), nullable=False)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider, name="payment_provider"),
        nullable=False,
        server_default=PaymentProvider.RAZORPAY.value,
    )
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        nullable=False,
        server_default=PaymentStatus.INITIATED.value,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, server_default="INR")
    receipt_number: Mapped[str | None] = mapped_column(String(120), nullable=True, unique=True)
    provider_order_id: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    provider_payment_id: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    provider_signature: Mapped[str | None] = mapped_column(String(500), nullable=True)
    provider_status_raw: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    application: Mapped[Application] = relationship("Application", back_populates="payments")
    user: Mapped[User | None] = relationship("User", back_populates="payments")
