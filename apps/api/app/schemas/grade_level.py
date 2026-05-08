"""Schemas for Grade Level management."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class GradeLevelBase(BaseModel):
    """Base schema for grade level."""

    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=120)
    display_order: int = Field(default=0, ge=0)
    default_fee: Optional[Decimal] = Field(None, ge=0)

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class GradeLevelCreate(GradeLevelBase):
    """Schema for creating grade level."""

    subject_id: UUID
    is_active: bool = Field(default=True)


class GradeLevelUpdate(BaseModel):
    """Schema for updating grade level."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=120)
    display_order: Optional[int] = Field(None, ge=0)
    default_fee: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class GradeLevelResponse(GradeLevelBase):
    """Schema for grade level response."""

    id: UUID
    subject_id: Optional[UUID]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GradeLevelListResponse(BaseModel):
    """Schema for paginated grade level list."""

    items: list[GradeLevelResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        from_attributes = True
