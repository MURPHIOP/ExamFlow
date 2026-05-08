"""Tests for payment operations."""
import json
from decimal import Decimal
from uuid import uuid4

import pytest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.enums import ApplicationStatus, PaymentStatus, PaymentProvider
from app.models.user import User
from app.repositories.payment_repository import PaymentRepository
from app.services.payment_service import PaymentService
from app.services.razorpay_service import RazorpayService
from app.services.receipt_number_service import ReceiptNumberService


class TestPaymentRepository:
    """Test PaymentRepository."""

    def test_create_payment_attempt(self, db: Session, test_student_user: User):
        """Test creating a payment attempt."""
        application_id = uuid4()
        repo = PaymentRepository(db)

        payment = repo.create_payment_attempt(
            application_id=application_id,
            user_id=test_student_user.id,
            amount=500.00,
            currency="INR",
            provider="razorpay",
        )

        assert payment.application_id == application_id
        assert payment.user_id == test_student_user.id
        assert payment.amount == Decimal("500.00")
        assert payment.provider == PaymentProvider.RAZORPAY
        assert payment.status == PaymentStatus.INITIATED

    def test_get_by_id(self, db: Session, test_student_user: User):
        """Test retrieving payment by ID."""
        application_id = uuid4()
        repo = PaymentRepository(db)

        payment = repo.create_payment_attempt(
            application_id=application_id,
            user_id=test_student_user.id,
            amount=500.00,
        )
        repo.commit()

        retrieved = repo.get_by_id(payment.id)
        assert retrieved is not None
        assert retrieved.id == payment.id

    def test_exists_success_for_application(
        self, db: Session, test_student_user: User
    ):
        """Test checking for existing successful payment."""
        application_id = uuid4()
        repo = PaymentRepository(db)

        # Initially no success payment
        assert not repo.exists_success_for_application(application_id)

        # Create and mark as success
        payment = repo.create_payment_attempt(
            application_id=application_id,
            user_id=test_student_user.id,
            amount=500.00,
        )
        repo.mark_success(
            payment_id=payment.id,
            provider_payment_id="pay_test123",
            provider_signature="sig_test123",
        )
        repo.commit()

        # Now should exist
        assert repo.exists_success_for_application(application_id)


class TestReceiptNumberService:
    """Test ReceiptNumberService."""

    def test_generate_unique_receipt_number(self, db: Session):
        """Test generating unique receipt numbers."""
        service = ReceiptNumberService(db)

        receipt1 = service.generate_receipt_number(year=2026)
        assert receipt1.startswith("MBT-RCPT-2026-")
        assert len(receipt1) == 19  # MBT-RCPT-2026-XXXXXX

    def test_receipt_number_format(self, db: Session):
        """Test receipt number format."""
        service = ReceiptNumberService(db)

        receipt = service.generate_receipt_number(year=2026)
        parts = receipt.split("-")
        assert len(parts) == 4
        assert parts[0] == "MBT"
        assert parts[1] == "RCPT"
        assert parts[2] == "2026"
        assert parts[3].isdigit()
        assert len(parts[3]) == 6


class TestRazorpayService:
    """Test RazorpayService."""

    @patch("app.services.razorpay_service.razorpay.Client")
    def test_verify_checkout_signature(self, mock_client):
        """Test Razorpay checkout signature verification."""
        service = RazorpayService()

        # Test valid signature
        order_id = "order_test123"
        payment_id = "pay_test456"
        # This is a valid HMAC signature for the above data using a test key
        # In real tests, this should be generated properly
        import hmac
        import hashlib

        test_secret = service.key_secret
        data = f"{order_id}|{payment_id}"
        signature = hmac.new(
            test_secret.encode(),
            data.encode(),
            hashlib.sha256,
        ).hexdigest()

        is_valid = service.verify_checkout_signature(
            razorpay_order_id=order_id,
            razorpay_payment_id=payment_id,
            razorpay_signature=signature,
        )
        assert is_valid

    @patch("app.services.razorpay_service.razorpay.Client")
    def test_verify_invalid_signature(self, mock_client):
        """Test invalid signature rejection."""
        service = RazorpayService()

        is_valid = service.verify_checkout_signature(
            razorpay_order_id="order_test123",
            razorpay_payment_id="pay_test456",
            razorpay_signature="invalid_signature_here",
        )
        assert not is_valid

    def test_verify_webhook_signature(self):
        """Test webhook signature verification."""
        service = RazorpayService()

        import hmac
        import hashlib

        request_body = b'{"event": "payment.captured"}'
        webhook_secret = service.webhook_secret or "test_secret"

        signature = hmac.new(
            webhook_secret.encode(),
            request_body,
            hashlib.sha256,
        ).hexdigest()

        is_valid = service.verify_webhook_signature(request_body, signature)
        assert is_valid

    def test_parse_webhook_payload(self):
        """Test parsing webhook payload."""
        service = RazorpayService()

        payload_dict = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "id": "pay_test123",
                    "order_id": "order_test456",
                    "amount": 50000,
                    "status": "captured",
                }
            },
        }
        payload_bytes = json.dumps(payload_dict).encode()

        parsed = service.parse_webhook_payload(payload_bytes)
        assert parsed["event"] == "payment.captured"
        assert parsed["payload"]["payment"]["id"] == "pay_test123"


class TestPaymentService:
    """Test PaymentService integration."""

    @patch("app.services.payment_service.RazorpayService.create_order")
    def test_create_payment_order_success(
        self,
        mock_create_order,
        db: Session,
        test_student_user: User,
        test_application_payment_pending: Application,
    ):
        """Test creating payment order for payment_pending application."""
        # Mock Razorpay order creation
        mock_order = {
            "id": "order_test123",
            "amount": 50000,
            "currency": "INR",
            "status": "created",
        }
        mock_create_order.return_value = mock_order

        service = PaymentService(db)

        result = service.create_payment_order(
            application_id=test_application_payment_pending.id,
            user_id=test_student_user.id,
            user_email=test_student_user.email,
            user_name=test_student_user.full_name,
        )

        assert result["razorpay_order_id"] == "order_test123"
        assert result["amount"] == "500.00"
        assert result["status"] == "initiated"
        assert result["key_id"] is not None

    def test_create_payment_order_not_owner(
        self, db: Session, test_admin_user: User, test_application_payment_pending: Application
    ):
        """Test that non-owner cannot create payment order."""
        service = PaymentService(db)

        with pytest.raises(ValueError, match="do not own"):
            service.create_payment_order(
                application_id=test_application_payment_pending.id,
                user_id=test_admin_user.id,
            )

    def test_create_payment_order_wrong_status(
        self,
        db: Session,
        test_student_user: User,
        test_application_draft: Application,
    ):
        """Test that draft application cannot create payment order."""
        service = PaymentService(db)

        with pytest.raises(ValueError, match="payment_pending"):
            service.create_payment_order(
                application_id=test_application_draft.id,
                user_id=test_student_user.id,
            )

    def test_duplicate_payment_blocked(
        self,
        db: Session,
        test_student_user: User,
        test_application_paid: Application,
    ):
        """Test that duplicate successful payment is blocked."""
        service = PaymentService(db)

        with pytest.raises(ValueError, match="already been paid"):
            service.create_payment_order(
                application_id=test_application_paid.id,
                user_id=test_student_user.id,
            )

    @patch("app.services.payment_service.RazorpayService.verify_checkout_signature")
    def test_verify_payment_success(
        self,
        mock_verify_sig,
        db: Session,
        test_student_user: User,
        test_payment_initiated,
    ):
        """Test successful payment verification."""
        mock_verify_sig.return_value = True

        service = PaymentService(db)

        result = service.verify_payment(
            application_id=test_payment_initiated.application_id,
            razorpay_order_id=test_payment_initiated.provider_order_id,
            razorpay_payment_id="pay_verified123",
            razorpay_signature="sig_valid",
            user_id=test_student_user.id,
        )

        assert result["payment"]["status"] == "success"
        assert result["payment"]["receipt_number"] is not None
        assert result["application"]["status"] == "paid"

    @patch("app.services.payment_service.RazorpayService.verify_checkout_signature")
    def test_verify_payment_invalid_signature(
        self,
        mock_verify_sig,
        db: Session,
        test_student_user: User,
        test_payment_initiated,
    ):
        """Test payment verification with invalid signature."""
        mock_verify_sig.return_value = False

        service = PaymentService(db)

        with pytest.raises(ValueError, match="signature verification failed"):
            service.verify_payment(
                application_id=test_payment_initiated.application_id,
                razorpay_order_id=test_payment_initiated.provider_order_id,
                razorpay_payment_id="pay_invalid123",
                razorpay_signature="sig_invalid",
                user_id=test_student_user.id,
            )

    def test_list_user_payments(
        self, db: Session, test_student_user: User, test_payment_success
    ):
        """Test listing user payments."""
        service = PaymentService(db)

        result = service.list_user_payments(
            user_id=test_student_user.id,
            page=1,
            page_size=20,
        )

        assert result["total"] >= 1
        assert len(result["items"]) >= 1
        assert result["items"][0]["status"] == "success"

    def test_list_admin_payments(self, db: Session, test_payment_success):
        """Test admin listing all payments."""
        service = PaymentService(db)

        result = service.list_admin_payments(
            page=1,
            page_size=20,
        )

        assert result["total"] >= 1
        assert len(result["items"]) >= 1


# Fixtures for payment tests
@pytest.fixture
def test_application_payment_pending(
    db: Session,
    test_student_user: User,
    test_exam_session,
    test_subject,
    test_grade_level,
    test_exam_fee,
):
    """Create an application in payment_pending status."""
    from app.models.application import Application

    app = Application(
        student_user_id=test_student_user.id,
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        grade_level_id=test_grade_level.id,
        status=ApplicationStatus.PAYMENT_PENDING,
        fee_amount=Decimal("500.00"),
        application_number=f"MBT-BSP-2026-{test_student_user.id.hex[:6].upper()}",
    )
    db.add(app)
    db.commit()
    return app


@pytest.fixture
def test_application_draft(db: Session, test_student_user: User, test_exam_session, test_subject):
    """Create a draft application."""
    from app.models.application import Application

    app = Application(
        student_user_id=test_student_user.id,
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        status=ApplicationStatus.DRAFT,
        fee_amount=Decimal("500.00"),
        application_number=f"MBT-BSP-2026-{uuid4().hex[:6].upper()}",
    )
    db.add(app)
    db.commit()
    return app


@pytest.fixture
def test_application_paid(
    db: Session,
    test_student_user: User,
    test_exam_session,
    test_subject,
    test_grade_level,
):
    """Create an application in paid status."""
    from app.models.application import Application

    app = Application(
        student_user_id=test_student_user.id,
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        grade_level_id=test_grade_level.id,
        status=ApplicationStatus.PAID,
        fee_amount=Decimal("500.00"),
        application_number=f"MBT-BSP-2026-{uuid4().hex[:6].upper()}",
    )
    db.add(app)
    db.commit()
    return app


@pytest.fixture
def test_payment_initiated(db: Session, test_application_payment_pending: Application):
    """Create a payment in initiated status."""
    from app.models.payment import Payment

    payment = Payment(
        application_id=test_application_payment_pending.id,
        user_id=test_application_payment_pending.student_user_id,
        provider=PaymentProvider.RAZORPAY,
        status=PaymentStatus.INITIATED,
        amount=test_application_payment_pending.fee_amount,
        currency="INR",
        provider_order_id="order_test_init123",
        provider_status_raw={"id": "order_test_init123", "status": "created"},
    )
    db.add(payment)
    db.commit()
    return payment


@pytest.fixture
def test_payment_success(db: Session, test_application_payment_pending: Application):
    """Create a payment in success status."""
    from app.models.payment import Payment
    from datetime import datetime

    payment = Payment(
        application_id=test_application_payment_pending.id,
        user_id=test_application_payment_pending.student_user_id,
        provider=PaymentProvider.RAZORPAY,
        status=PaymentStatus.SUCCESS,
        amount=test_application_payment_pending.fee_amount,
        currency="INR",
        provider_order_id="order_test_success123",
        provider_payment_id="pay_test_success123",
        provider_signature="sig_test_success123",
        receipt_number="MBT-RCPT-2026-000001",
        paid_at=datetime.utcnow(),
    )
    db.add(payment)
    db.commit()
    return payment
