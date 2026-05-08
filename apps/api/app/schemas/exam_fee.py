"""Schemas for Exam Fee management."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ExamFeeBase(BaseModel):
    """Base schema for exam fee."""

    amount: Decimal = Field(..., ge=0)
    currency: str = Field(default="INR", max_length=10)
    late_fee_amount: Decimal = Field(default=Decimal("0"), ge=0)

    @field_validator("amount", "late_fee_amount", mode="before")
    @classmethod
    def decimal_to_decimal(cls, v):
        """Convert to Decimal if needed."""
        if v is not None:
            return Decimal(str(v))
        return v


class ExamFeeCreate(ExamFeeBase):
    """Schema for creating exam fee."""

    exam_session_id: UUID
    subject_id: UUID
    grade_level_id: Optional[UUID] = None
    is_active: bool = Field(default=True)


class ExamFeeUpdate(BaseModel):
    """Schema for updating exam fee."""

    amount: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=10)
    late_fee_amount: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None

    @field_validator("amount", "late_fee_amount", mode="before")
    @classmethod
    def decimal_to_decimal(cls, v):
        """Convert to Decimal if needed."""
        if v is not None:
            return Decimal(str(v))
        return v


class ExamFeeResponse(ExamFeeBase):
    """Schema for exam fee response."""

    id: UUID
    exam_session_id: UUID
    subject_id: UUID
    grade_level_id: Optional[UUID]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamFeeListResponse(BaseModel):
    """Schema for paginated exam fee list."""

    items: list[ExamFeeResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        from_attributes = True


class ExamFeeLookupResponse(BaseModel):
    """Schema for fee lookup response."""

    id: UUID
    amount: Decimal
    currency: str
    late_fee_amount: Decimal
    exam_session_id: UUID
    subject_id: UUID
    grade_level_id: Optional[UUID]

    class Config:
        from_attributes = True
