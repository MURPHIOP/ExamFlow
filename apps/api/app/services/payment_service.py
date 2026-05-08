"""Service for payment operations and workflow."""
import logging
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.enums import ApplicationStatus, PaymentStatus, PaymentProvider
from app.repositories.application_repository import ApplicationRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.application_status_service import ApplicationStatusService
from app.services.razorpay_service import RazorpayService
from app.services.receipt_number_service import ReceiptNumberService
from app.services.audit_service import AuditService

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for managing payment operations."""

    def __init__(self, db: Session):
        """Initialize payment service."""
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.application_repo = ApplicationRepository(db)
        self.razorpay_service = RazorpayService()
        self.receipt_service = ReceiptNumberService(db)
        self.status_service = ApplicationStatusService()
        self.audit_service = AuditService(db)

    def create_payment_order(
        self,
        application_id: UUID,
        user_id: UUID,
        user_email: Optional[str] = None,
        user_phone: Optional[str] = None,
        user_name: Optional[str] = None,
    ) -> dict:
        """Create a Razorpay payment order for a payment_pending application.

        Args:
            application_id: Application UUID
            user_id: User making the payment
            user_email: User email for prefill
            user_phone: User phone for prefill
            user_name: User name for prefill

        Returns:
            Payment order response with Razorpay checkout data

        Raises:
            ValueError: If validation fails
        """
        try:
            # Get application
            application = self.application_repo.get_by_id(application_id)
            if not application:
                raise ValueError(f"Application {application_id} not found")

            # Verify ownership
            if application.student_user_id != user_id:
                raise ValueError("You do not own this application")

            # Check application status is payment_pending
            if application.status != ApplicationStatus.PAYMENT_PENDING:
                raise ValueError(
                    f"Application must be in payment_pending status, current: {application.status}"
                )

            # Check fee_amount > 0
            if not application.fee_amount or application.fee_amount <= 0:
                raise ValueError("Application has no fee or fee is zero")

            # Check no successful payment already exists
            if self.payment_repo.exists_success_for_application(application_id):
                raise ValueError("This application has already been paid")

            # Check for existing pending/initiated payment and reuse if valid
            latest_payment = self.payment_repo.get_latest_by_application_id(
                application_id
            )
            if latest_payment and latest_payment.status in [
                PaymentStatus.INITIATED,
                PaymentStatus.PENDING,
            ]:
                # Reuse pending order
                if latest_payment.provider_order_id:
                    logger.info(
                        f"Reusing pending order {latest_payment.provider_order_id}"
                    )
                    payment = latest_payment
                else:
                    payment = self._create_new_payment_and_order(
                        application_id, user_id, application
                    )
            else:
                payment = self._create_new_payment_and_order(
                    application_id, user_id, application
                )

            # Prepare checkout data
            amount_paise = int(application.fee_amount * 100)
            checkout_data = {
                "payment_id": str(payment.id),
                "application_id": str(application_id),
                "application_number": application.application_number,
                "razorpay_order_id": payment.provider_order_id,
                "amount": str(application.fee_amount),
                "amount_paise": amount_paise,
                "currency": payment.currency,
                "status": payment.status,
                "key_id": self.razorpay_service.key_id,
                "checkout_prefill": {
                    "name": user_name,
                    "email": user_email,
                    "contact": user_phone,
                },
            }

            # Audit
            self.audit_service.log_action(
                action="PAYMENT_ORDER_CREATED",
                entity_type="payment",
                actor_user_id=user_id,
                entity_id=payment.id,
                metadata={
                    "application_id": str(application_id),
                    "amount": str(application.fee_amount),
                    "razorpay_order_id": payment.provider_order_id,
                },
            )

            self.payment_repo.commit()
            return checkout_data

        except Exception as e:
            logger.error(f"Failed to create payment order: {str(e)}")
            self.payment_repo.rollback()
            raise

    def _create_new_payment_and_order(
        self, application_id: UUID, user_id: UUID, application: Application
    ):
        """Helper to create new payment record and Razorpay order."""
        # Create Razorpay order
        amount_paise = int(application.fee_amount * 100)
        razorpay_order = self.razorpay_service.create_order(
            amount_paise=amount_paise,
            receipt=f"app-{application.application_number}",
            notes={
                "application_id": str(application_id),
                "application_number": application.application_number,
            },
        )

        # Create payment record
        payment = self.payment_repo.create_payment_attempt(
            application_id=application_id,
            user_id=user_id,
            amount=float(application.fee_amount),
            currency="INR",
            provider="razorpay",
        )

        # Update payment with provider order ID
        payment.provider_order_id = razorpay_order["id"]
        payment.provider_status_raw = razorpay_order
        payment.status = PaymentStatus.INITIATED
        self.payment_repo.flush()
        return payment

    def verify_payment(
        self,
        application_id: UUID,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
        user_id: UUID,
    ) -> dict:
        """Verify a Razorpay payment after checkout.

        Args:
            application_id: Application UUID
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Signature from Razorpay
            user_id: User making the payment

        Returns:
            Payment and application status update

        Raises:
            ValueError: If verification fails
        """
        try:
            # Get application
            application = self.application_repo.get_by_id(application_id)
            if not application:
                raise ValueError(f"Application {application_id} not found")

            # Verify ownership
            if application.student_user_id != user_id:
                raise ValueError("You do not own this application")

            # Get payment
            payment = self.payment_repo.get_by_provider_order_id(razorpay_order_id)
            if not payment:
                raise ValueError(
                    f"Payment order {razorpay_order_id} not found"
                )

            # Verify amount matches
            if payment.amount != application.fee_amount:
                logger.error(
                    f"Amount mismatch: payment={payment.amount}, "
                    f"application_fee={application.fee_amount}"
                )
                raise ValueError("Payment amount does not match application fee")

            # Check no successful payment already exists
            if self.payment_repo.exists_success_for_application(application_id):
                raise ValueError("This application has already been paid")

            # Verify signature
            is_valid = self.razorpay_service.verify_checkout_signature(
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature,
            )

            if not is_valid:
                self.audit_service.log_action(
                    action="PAYMENT_VERIFICATION_FAILED",
                    entity_type="payment",
                    actor_user_id=user_id,
                    entity_id=payment.id,
                    metadata={
                        "application_id": str(application_id),
                        "reason": "Invalid signature",
                    },
                )
                self.payment_repo.mark_failed(payment.id, "Invalid signature")
                self.payment_repo.commit()
                raise ValueError("Payment signature verification failed")

            # Generate receipt number
            receipt_number = self.receipt_service.generate_receipt_number(
                year=application.exam_session.year if application.exam_session else None
            )

            # Mark payment as success
            self.payment_repo.mark_success(
                payment_id=payment.id,
                provider_payment_id=razorpay_payment_id,
                provider_signature=razorpay_signature,
                receipt_number=receipt_number,
            )

            # Update application status: payment_pending -> paid
            self.application_repo.update_status(
                application_id=application_id,
                new_status=ApplicationStatus.PAID,
            )

            # Audit
            self.audit_service.log_action(
                action="PAYMENT_VERIFICATION_SUCCESS",
                entity_type="payment",
                actor_user_id=user_id,
                entity_id=payment.id,
                metadata={
                    "application_id": str(application_id),
                    "receipt_number": receipt_number,
                    "razorpay_payment_id": razorpay_payment_id,
                },
            )

            self.audit_service.log_action(
                action="PAYMENT_STATUS_UPDATED",
                entity_type="application",
                actor_user_id=user_id,
                entity_id=application_id,
                metadata={
                    "old_status": ApplicationStatus.PAYMENT_PENDING,
                    "new_status": ApplicationStatus.PAID,
                    "reason": "Payment verified and successful",
                },
            )

            self.payment_repo.commit()

            return {
                "payment": {
                    "id": str(payment.id),
                    "status": payment.status,
                    "amount": str(payment.amount),
                    "receipt_number": receipt_number,
                },
                "application": {
                    "id": str(application_id),
                    "application_number": application.application_number,
                    "status": ApplicationStatus.PAID,
                },
            }

        except Exception as e:
            logger.error(f"Payment verification failed: {str(e)}")
            self.payment_repo.rollback()
            raise

    def handle_webhook(self, webhook_payload: dict, user_id: Optional[UUID] = None) -> dict:
        """Handle Razorpay webhook events.

        Args:
            webhook_payload: Parsed webhook JSON payload
            user_id: Optional user ID for logging

        Returns:
            Webhook processing result

        Raises:
            ValueError: If processing fails
        """
        try:
            event = webhook_payload.get("event")
            event_data = webhook_payload.get("payload", {}).get("payment", {})

            logger.info(f"Processing webhook event: {event}")

            if event == "payment.captured":
                return self._handle_payment_captured(event_data, user_id)
            elif event == "payment.failed":
                return self._handle_payment_failed(event_data, user_id)
            elif event == "order.paid":
                return self._handle_order_paid(event_data, user_id)
            else:
                logger.info(f"Ignoring webhook event: {event}")
                return {"received": True, "processed": False, "event": event}

        except Exception as e:
            logger.error(f"Webhook processing failed: {str(e)}")
            raise

    def _handle_payment_captured(self, event_data: dict, user_id: Optional[UUID]) -> dict:
        """Handle payment.captured webhook event."""
        razorpay_payment_id = event_data.get("id")
        razorpay_order_id = event_data.get("order_id")

        if not razorpay_payment_id or not razorpay_order_id:
            raise ValueError("Missing payment or order ID in webhook")

        # Check if already processed
        payment = self.payment_repo.get_by_provider_payment_id(razorpay_payment_id)
        if payment and payment.status == PaymentStatus.SUCCESS:
            logger.info(f"Payment {razorpay_payment_id} already processed")
            return {"received": True, "processed": False, "event": "payment.captured"}

        # Get or create payment record
        if not payment:
            payment = self.payment_repo.get_by_provider_order_id(razorpay_order_id)
            if not payment:
                logger.warning(
                    f"Payment order {razorpay_order_id} not found in webhook"
                )
                return {"received": True, "processed": False, "event": "payment.captured"}

        # Generate receipt if not exists
        receipt_number = payment.receipt_number or (
            self.receipt_service.generate_receipt_number()
        )

        # Mark as success
        payment.status = PaymentStatus.SUCCESS
        payment.provider_payment_id = razorpay_payment_id
        payment.receipt_number = receipt_number

        # Update application status
        self.application_repo.update_status(
            application_id=payment.application_id,
            new_status=ApplicationStatus.PAID,
        )

        # Audit
        self.audit_service.log_action(
            action="PAYMENT_WEBHOOK_PROCESSED",
            entity_type="payment",
            actor_user_id=user_id,
            entity_id=payment.id,
            metadata={
                "event": "payment.captured",
                "razorpay_payment_id": razorpay_payment_id,
                "receipt_number": receipt_number,
            },
        )

        self.payment_repo.commit()
        return {"received": True, "processed": True, "event": "payment.captured"}

    def _handle_payment_failed(self, event_data: dict, user_id: Optional[UUID]) -> dict:
        """Handle payment.failed webhook event."""
        razorpay_payment_id = event_data.get("id")
        failure_reason = event_data.get("description", "Unknown reason")

        if not razorpay_payment_id:
            raise ValueError("Missing payment ID in webhook")

        # Get payment
        payment = self.payment_repo.get_by_provider_payment_id(razorpay_payment_id)
        if not payment:
            logger.warning(f"Payment {razorpay_payment_id} not found in webhook")
            return {"received": True, "processed": False, "event": "payment.failed"}

        # Mark as failed
        payment.status = PaymentStatus.FAILED
        payment.failure_reason = failure_reason

        # Audit
        self.audit_service.log_action(
            action="PAYMENT_WEBHOOK_PROCESSED",
            entity_type="payment",
            actor_user_id=user_id,
            entity_id=payment.id,
            metadata={
                "event": "payment.failed",
                "failure_reason": failure_reason,
            },
        )

        self.payment_repo.commit()
        return {"received": True, "processed": True, "event": "payment.failed"}

    def _handle_order_paid(self, event_data: dict, user_id: Optional[UUID]) -> dict:
        """Handle order.paid webhook event."""
        razorpay_order_id = event_data.get("id")

        if not razorpay_order_id:
            raise ValueError("Missing order ID in webhook")

        # Get payment
        payment = self.payment_repo.get_by_provider_order_id(razorpay_order_id)
        if not payment:
            logger.warning(f"Payment order {razorpay_order_id} not found in webhook")
            return {"received": True, "processed": False, "event": "order.paid"}

        # Check if already marked success
        if payment.status == PaymentStatus.SUCCESS:
            return {"received": True, "processed": False, "event": "order.paid"}

        # Mark as success
        payment.status = PaymentStatus.SUCCESS
        payment.receipt_number = payment.receipt_number or (
            self.receipt_service.generate_receipt_number()
        )

        # Update application status
        self.application_repo.update_status(
            application_id=payment.application_id,
            new_status=ApplicationStatus.PAID,
        )

        # Audit
        self.audit_service.log_action(
            action="PAYMENT_WEBHOOK_PROCESSED",
            entity_type="payment",
            actor_user_id=user_id,
            entity_id=payment.id,
            metadata={
                "event": "order.paid",
                "receipt_number": payment.receipt_number,
            },
        )

        self.payment_repo.commit()
        return {"received": True, "processed": True, "event": "order.paid"}

    def get_payment(self, payment_id: UUID) -> Optional[dict]:
        """Get payment details."""
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            return None

        return {
            "id": str(payment.id),
            "application_id": str(payment.application_id),
            "provider": payment.provider,
            "status": payment.status,
            "amount": str(payment.amount),
            "currency": payment.currency,
            "receipt_number": payment.receipt_number,
            "provider_order_id": payment.provider_order_id,
            "provider_payment_id": payment.provider_payment_id,
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "created_at": payment.created_at.isoformat(),
            "updated_at": payment.updated_at.isoformat(),
        }

    def list_user_payments(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ) -> dict:
        """List payments for a user."""
        payments, total = self.payment_repo.list_for_user(
            user_id=user_id,
            page=page,
            page_size=page_size,
            status=status,
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [
                {
                    "id": str(p.id),
                    "application_id": str(p.application_id),
                    "provider": p.provider,
                    "status": p.status,
                    "amount": str(p.amount),
                    "currency": p.currency,
                    "receipt_number": p.receipt_number,
                    "paid_at": p.paid_at.isoformat() if p.paid_at else None,
                    "created_at": p.created_at.isoformat(),
                }
                for p in payments
            ],
        }

    def list_admin_payments(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> dict:
        """List all payments (admin view)."""
        payments, total = self.payment_repo.list_for_admin(
            page=page,
            page_size=page_size,
            status=status,
            provider=provider,
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [
                {
                    "id": str(p.id),
                    "application_id": str(p.application_id),
                    "user_id": str(p.user_id) if p.user_id else None,
                    "provider": p.provider,
                    "status": p.status,
                    "amount": str(p.amount),
                    "currency": p.currency,
                    "receipt_number": p.receipt_number,
                    "provider_order_id": p.provider_order_id,
                    "paid_at": p.paid_at.isoformat() if p.paid_at else None,
                    "created_at": p.created_at.isoformat(),
                }
                for p in payments
            ],
        }
