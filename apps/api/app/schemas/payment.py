"""Schemas for payment operations."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PaymentOrderCreateRequest(BaseModel):
    """Request to create a Razorpay payment order."""

    application_id: UUID = Field(..., description="Application UUID")


class CheckoutPrefill(BaseModel):
    """Razorpay checkout prefill data."""

    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None


class PaymentOrderResponse(BaseModel):
    """Response from creating a payment order."""

    payment_id: UUID = Field(..., description="Internal payment ID")
    application_id: UUID
    application_number: str
    razorpay_order_id: str
    amount: str = Field(..., description="Amount in rupees")
    amount_paise: int = Field(..., description="Amount in paise for Razorpay")
    currency: str = "INR"
    status: str
    key_id: str = Field(..., description="Razorpay public key")
    checkout_prefill: Optional[CheckoutPrefill] = None

    model_config = ConfigDict(from_attributes=True)


class PaymentVerifyRequest(BaseModel):
    """Request to verify a Razorpay payment."""

    application_id: UUID
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentResponse(BaseModel):
    """Payment details response."""

    id: UUID
    application_id: UUID
    provider: str
    status: str
    amount: Decimal = Field(..., description="Amount in rupees")
    currency: str = "INR"
    receipt_number: Optional[str] = None
    provider_order_id: Optional[str] = None
    provider_payment_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentListResponse(BaseModel):
    """Paginated payment list response."""

    total: int
    page: int
    page_size: int
    items: list[PaymentResponse]


class RazorpayWebhookResponse(BaseModel):
    """Response from webhook processing."""

    received: bool
    processed: bool
    event: Optional[str] = None


class ReceiptResponse(BaseModel):
    """Receipt metadata response."""

    receipt_number: str
    application_number: str
    student_name: str
    amount: Decimal
    currency: str = "INR"
    paid_at: datetime
    payment_id: UUID
    provider: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class ReceiptDetailResponse(BaseModel):
    """Detailed receipt response for display."""

    receipt_number: str
    application_number: str
    student_name: str
    student_email: Optional[str] = None
    student_phone: Optional[str] = None
    exam_session_name: str
    subject_name: str
    grade_level_name: str
    amount: Decimal
    currency: str = "INR"
    paid_at: datetime
    payment_id: UUID
    provider: str
    provider_payment_id: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)
