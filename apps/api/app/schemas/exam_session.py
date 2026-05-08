"""Schemas for Exam Session management."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ExamSessionBase(BaseModel):
    """Base schema for exam session."""

    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=120)
    year: int = Field(..., ge=2000, le=2100)
    description: Optional[str] = Field(None, max_length=1000)
    application_start_date: Optional[datetime] = None
    application_end_date: Optional[datetime] = None
    exam_start_date: Optional[datetime] = None
    exam_end_date: Optional[datetime] = None
    result_publish_date: Optional[datetime] = None
    certificate_issue_date: Optional[datetime] = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v

    @field_validator("application_end_date")
    @classmethod
    def validate_application_dates(cls, v, info):
        """Validate application end date is not before start date."""
        if v and "application_start_date" in info.data:
            if info.data.get("application_start_date") and v < info.data["application_start_date"]:
                raise ValueError("application_end_date cannot be before application_start_date")
        return v

    @field_validator("exam_end_date")
    @classmethod
    def validate_exam_dates(cls, v, info):
        """Validate exam end date is not before start date."""
        if v and "exam_start_date" in info.data:
            if info.data.get("exam_start_date") and v < info.data["exam_start_date"]:
                raise ValueError("exam_end_date cannot be before exam_start_date")
        return v


class ExamSessionCreate(ExamSessionBase):
    """Schema for creating exam session."""

    status: str = Field(default="draft")


class ExamSessionUpdate(BaseModel):
    """Schema for updating exam session."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=120)
    year: Optional[int] = Field(None, ge=2000, le=2100)
    description: Optional[str] = Field(None, max_length=1000)
    application_start_date: Optional[datetime] = None
    application_end_date: Optional[datetime] = None
    exam_start_date: Optional[datetime] = None
    exam_end_date: Optional[datetime] = None
    result_publish_date: Optional[datetime] = None
    certificate_issue_date: Optional[datetime] = None
    status: Optional[str] = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class ExamSessionResponse(ExamSessionBase):
    """Schema for exam session response."""

    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamSessionListResponse(BaseModel):
    """Schema for paginated exam session list."""

    items: list[ExamSessionResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        from_attributes = True
