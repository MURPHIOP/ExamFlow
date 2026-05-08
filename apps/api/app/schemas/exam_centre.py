"""Schemas for Exam Centre management."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ExamCentreBase(BaseModel):
    """Base schema for exam centre."""

    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=120)
    address_line_1: str = Field(..., min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    district: Optional[str] = Field(None, max_length=120)
    state: Optional[str] = Field(None, max_length=120)
    pincode: Optional[str] = Field(None, max_length=20)
    contact_person_name: Optional[str] = Field(None, max_length=255)
    contact_person_phone: Optional[str] = Field(None, max_length=20)
    capacity: int = Field(default=0, ge=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class ExamCentreCreate(ExamCentreBase):
    """Schema for creating exam centre."""

    status: str = Field(default="active")


class ExamCentreUpdate(BaseModel):
    """Schema for updating exam centre."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=120)
    address_line_1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    district: Optional[str] = Field(None, max_length=120)
    state: Optional[str] = Field(None, max_length=120)
    pincode: Optional[str] = Field(None, max_length=20)
    contact_person_name: Optional[str] = Field(None, max_length=255)
    contact_person_phone: Optional[str] = Field(None, max_length=20)
    capacity: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class ExamCentreResponse(ExamCentreBase):
    """Schema for exam centre response."""

    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamCentreListResponse(BaseModel):
    """Schema for paginated exam centre list."""

    items: list[ExamCentreResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        from_attributes = True
