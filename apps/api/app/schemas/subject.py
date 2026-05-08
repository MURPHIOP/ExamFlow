"""Schemas for Subject management."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class SubjectBase(BaseModel):
    """Base schema for subject."""

    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=120)
    category: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class SubjectCreate(SubjectBase):
    """Schema for creating subject."""

    is_active: bool = Field(default=True)


class SubjectUpdate(BaseModel):
    """Schema for updating subject."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=120)
    category: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None

    @field_validator("code")
    @classmethod
    def code_uppercase(cls, v):
        """Ensure code is uppercase."""
        if v:
            v = v.upper()
        return v


class SubjectResponse(SubjectBase):
    """Schema for subject response."""

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubjectListResponse(BaseModel):
    """Schema for paginated subject list."""

    items: list[SubjectResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        from_attributes = True
