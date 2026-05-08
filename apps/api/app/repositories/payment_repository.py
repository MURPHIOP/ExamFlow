"""Repository for Payment operations."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.enums import PaymentStatus


class PaymentRepository:
    """Data access layer for Payment model."""

    def __init__(self, db: Session):
        self.db = db

    def create_payment_attempt(
        self,
        application_id: UUID,
        user_id: Optional[UUID],
        amount: float,
        currency: str = "INR",
        provider: str = "razorpay",
    ) -> Payment:
        """Create a new payment attempt."""
        payment = Payment(
            application_id=application_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            provider=provider,
        )
        self.db.add(payment)
        return payment

    def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        """Get payment by ID."""
        stmt = select(Payment).where(Payment.id == payment_id)
        return self.db.scalar(stmt)

    def get_by_application_id(self, application_id: UUID) -> list[Payment]:
        """Get all payments for an application."""
        stmt = (
            select(Payment)
            .where(Payment.application_id == application_id)
            .order_by(desc(Payment.created_at))
        )
        return self.db.scalars(stmt).all()

    def get_latest_by_application_id(self, application_id: UUID) -> Optional[Payment]:
        """Get latest payment for an application."""
        stmt = (
            select(Payment)
            .where(Payment.application_id == application_id)
            .order_by(desc(Payment.created_at))
            .limit(1)
        )
        return self.db.scalar(stmt)

    def get_by_provider_order_id(self, provider_order_id: str) -> Optional[Payment]:
        """Get payment by provider order ID (e.g., Razorpay order ID)."""
        stmt = select(Payment).where(Payment.provider_order_id == provider_order_id)
        return self.db.scalar(stmt)

    def get_by_provider_payment_id(self, provider_payment_id: str) -> Optional[Payment]:
        """Get payment by provider payment ID (e.g., Razorpay payment ID)."""
        stmt = select(Payment).where(Payment.provider_payment_id == provider_payment_id)
        return self.db.scalar(stmt)

    def exists_success_for_application(self, application_id: UUID) -> bool:
        """Check if a successful payment already exists for this application."""
        stmt = select(
            func.count(Payment.id)
        ).where(
            and_(
                Payment.application_id == application_id,
                Payment.status == PaymentStatus.SUCCESS,
            )
        )
        count = self.db.scalar(stmt) or 0
        return count > 0

    def list_for_user(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> tuple[list[Payment], int]:
        """List payments for a user with pagination."""
        query = select(Payment).where(Payment.user_id == user_id)

        if status:
            query = query.where(Payment.status == status)

        # Get total count
        count_stmt = select(func.count(Payment.id)).select_from(Payment)
        if status:
            count_stmt = count_stmt.where(Payment.status == status)
        total = self.db.scalar(count_stmt) or 0

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.order_by(desc(Payment.created_at)).offset(offset).limit(page_size)

        payments = self.db.scalars(query).all()
        return payments, total

    def list_for_admin(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        provider: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> tuple[list[Payment], int]:
        """List all payments (admin view) with filters."""
        query = select(Payment)

        if status:
            query = query.where(Payment.status == status)
        if provider:
            query = query.where(Payment.provider == provider)
        if date_from:
            query = query.where(Payment.created_at >= date_from)
        if date_to:
            query = query.where(Payment.created_at <= date_to)

        # Get total count
        count_stmt = select(func.count(Payment.id)).select_from(Payment)
        if status:
            count_stmt = count_stmt.where(Payment.status == status)
        if provider:
            count_stmt = count_stmt.where(Payment.provider == provider)
        if date_from:
            count_stmt = count_stmt.where(Payment.created_at >= date_from)
        if date_to:
            count_stmt = count_stmt.where(Payment.created_at <= date_to)
        total = self.db.scalar(count_stmt) or 0

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.order_by(desc(Payment.created_at)).offset(offset).limit(page_size)

        payments = self.db.scalars(query).all()
        return payments, total

    def mark_success(
        self,
        payment_id: UUID,
        provider_payment_id: str,
        provider_signature: str,
        receipt_number: Optional[str] = None,
    ) -> Payment:
        """Mark payment as successful."""
        payment = self.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        payment.status = PaymentStatus.SUCCESS
        payment.provider_payment_id = provider_payment_id
        payment.provider_signature = provider_signature
        payment.receipt_number = receipt_number
        payment.paid_at = datetime.utcnow()
        return payment

    def mark_failed(
        self,
        payment_id: UUID,
        failure_reason: str,
    ) -> Payment:
        """Mark payment as failed."""
        payment = self.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        payment.status = PaymentStatus.FAILED
        payment.failure_reason = failure_reason
        return payment

    def update_provider_raw(
        self,
        payment_id: UUID,
        provider_order_id: str,
        provider_status_raw: dict,
    ) -> Payment:
        """Update payment with provider raw response data."""
        payment = self.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        payment.provider_order_id = provider_order_id
        payment.provider_status_raw = provider_status_raw
        return payment

    def set_receipt_number(self, payment_id: UUID, receipt_number: str) -> Payment:
        """Set receipt number for a payment."""
        payment = self.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")

        payment.receipt_number = receipt_number
        return payment

    def commit(self) -> None:
        """Commit database transaction."""
        self.db.commit()

    def flush(self) -> None:
        """Flush pending changes to database."""
        self.db.flush()

    def rollback(self) -> None:
        """Rollback database transaction."""
        self.db.rollback()
