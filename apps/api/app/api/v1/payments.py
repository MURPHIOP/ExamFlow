"""API routes for payment operations."""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_admin_or_super_admin
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.payment import (
    PaymentOrderCreateRequest,
    PaymentOrderResponse,
    PaymentVerifyRequest,
    PaymentResponse,
    PaymentListResponse,
    RazorpayWebhookResponse,
    ReceiptResponse,
)
from app.services.payment_service import PaymentService
from app.services.razorpay_service import RazorpayService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-order", response_model=ApiResponse, status_code=201)
async def create_payment_order(
    request: PaymentOrderCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a Razorpay payment order for a payment_pending application.

    Only students and institutions can create payment orders for their applications.
    """
    try:
        service = PaymentService(db)

        result = service.create_payment_order(
            application_id=request.application_id,
            user_id=current_user.id,
            user_email=current_user.email,
            user_phone=current_user.phone,
            user_name=current_user.full_name,
        )

        return ApiResponse(
            success=True,
            message="Payment order created successfully",
            data=result,
        )

    except ValueError as e:
        logger.warning(f"Validation error creating payment order: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating payment order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create payment order")


@router.post("/verify", response_model=ApiResponse)
async def verify_payment(
    request: PaymentVerifyRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Verify a Razorpay payment after checkout.

    Students and institutions can verify their own payments.
    """
    try:
        service = PaymentService(db)

        result = service.verify_payment(
            application_id=request.application_id,
            razorpay_order_id=request.razorpay_order_id,
            razorpay_payment_id=request.razorpay_payment_id,
            razorpay_signature=request.razorpay_signature,
            user_id=current_user.id,
        )

        return ApiResponse(
            success=True,
            message="Payment verified successfully",
            data=result,
        )

    except ValueError as e:
        logger.warning(f"Payment verification failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error verifying payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to verify payment")


@router.post("/webhook", response_model=ApiResponse)
async def handle_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """Handle Razorpay webhook events.

    This endpoint is public but protected by Razorpay webhook signature verification.
    """
    try:
        # Get raw request body
        raw_body = await request.body()

        # Verify webhook signature
        razorpay_service = RazorpayService()
        signature = request.headers.get("X-Razorpay-Signature", "")

        if not razorpay_service.verify_webhook_signature(raw_body, signature):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=400, detail="Invalid webhook signature")

        # Parse payload
        payload = razorpay_service.parse_webhook_payload(raw_body)

        # Process webhook
        service = PaymentService(db)
        result = service.handle_webhook(payload)

        return ApiResponse(
            success=True,
            message="Webhook processed",
            data=result,
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process webhook")


@router.get("/my", response_model=ApiResponse)
async def list_my_payments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """List current user's payments."""
    try:
        service = PaymentService(db)
        result = service.list_user_payments(
            user_id=current_user.id,
            page=page,
            page_size=page_size,
            status=status,
        )

        return ApiResponse(
            success=True,
            message="Payments retrieved successfully",
            data=result,
        )

    except Exception as e:
        logger.error(f"Error listing payments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list payments")


@router.get("/my/{payment_id}", response_model=ApiResponse)
async def get_my_payment(
    payment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current user's payment details."""
    try:
        service = PaymentService(db)
        payment_data = service.get_payment(payment_id)

        if not payment_data:
            raise HTTPException(status_code=404, detail="Payment not found")

        # Verify ownership
        from app.repositories.payment_repository import PaymentRepository

        repo = PaymentRepository(db)
        payment = repo.get_by_id(payment_id)
        if not payment or payment.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        return ApiResponse(
            success=True,
            message="Payment retrieved successfully",
            data=payment_data,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve payment")


@router.get("/admin", response_model=ApiResponse)
async def list_admin_payments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    provider: str = Query(None),
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """List all payments (admin view)."""
    try:
        service = PaymentService(db)
        result = service.list_admin_payments(
            page=page,
            page_size=page_size,
            status=status,
            provider=provider,
        )

        return ApiResponse(
            success=True,
            message="Payments retrieved successfully",
            data=result,
        )

    except Exception as e:
        logger.error(f"Error listing payments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list payments")


@router.get("/admin/{payment_id}", response_model=ApiResponse)
async def get_admin_payment(
    payment_id: UUID,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Get payment details (admin view)."""
    try:
        service = PaymentService(db)
        payment_data = service.get_payment(payment_id)

        if not payment_data:
            raise HTTPException(status_code=404, detail="Payment not found")

        return ApiResponse(
            success=True,
            message="Payment retrieved successfully",
            data=payment_data,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve payment")


@router.get("/{payment_id}/receipt", response_model=ApiResponse)
async def get_receipt_metadata(
    payment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get receipt metadata for a payment.

    Students can view receipts for their own payments.
    Admin/Super Admin can view any receipt.
    """
    try:
        from app.repositories.payment_repository import PaymentRepository
        from app.repositories.application_repository import ApplicationRepository

        payment_repo = PaymentRepository(db)
        app_repo = ApplicationRepository(db)

        payment = payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        # Verify access
        if (
            payment.status != "success"
            and payment.user_id != current_user.id
        ):
            raise HTTPException(status_code=403, detail="Access denied")

        # Get application
        application = app_repo.get_by_id(payment.application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        # Build receipt response
        receipt = {
            "receipt_number": payment.receipt_number,
            "application_number": application.application_number,
            "student_name": application.student.user.full_name if application.student else "N/A",
            "student_email": application.student.user.email
            if application.student else None,
            "student_phone": application.student.user.phone
            if application.student else None,
            "exam_session_name": (
                application.exam_session.name if application.exam_session else "N/A"
            ),
            "subject_name": application.subject.name if application.subject else "N/A",
            "grade_level_name": (
                application.grade_level.name if application.grade_level else "N/A"
            ),
            "amount": str(payment.amount),
            "currency": payment.currency,
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "payment_id": str(payment.id),
            "provider": payment.provider,
            "provider_payment_id": payment.provider_payment_id,
            "status": payment.status,
        }

        return ApiResponse(
            success=True,
            message="Receipt retrieved successfully",
            data=receipt,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving receipt: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve receipt")
