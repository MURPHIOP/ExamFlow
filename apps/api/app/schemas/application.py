"""Schemas for Application workflows."""
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import ApplicationStatus, Gender


class StudentDataForInstitutionCreate(BaseModel):
    """Student data for creating student profile during institution application."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[str] = None
    gender: Optional[Gender] = None
    guardian_name: Optional[str] = Field(None, max_length=255)
    guardian_phone: Optional[str] = Field(None, max_length=20)
    address_line_1: Optional[str] = Field(None, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    district: Optional[str] = Field(None, max_length=120)
    state: Optional[str] = Field(None, max_length=120)
    pincode: Optional[str] = Field(None, max_length=20)


class ApplicationCreate(BaseModel):
    """Schema for creating a student application."""

    exam_session_id: UUID
    subject_id: UUID
    grade_level_id: Optional[UUID] = None
    preferred_centre_id: Optional[UUID] = None
    student_notes: Optional[str] = None

    class Config:
        from_attributes = True


class InstitutionApplicationCreate(BaseModel):
    """Schema for creating an institution application."""

    student_user_id: Optional[UUID] = None
    existing_student_profile_id: Optional[UUID] = None
    student_data: Optional[StudentDataForInstitutionCreate] = None
    exam_session_id: UUID
    subject_id: UUID
    grade_level_id: Optional[UUID] = None
    preferred_centre_id: Optional[UUID] = None
    institution_notes: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    """Schema for updating an application (student/institution only)."""

    subject_id: Optional[UUID] = None
    grade_level_id: Optional[UUID] = None
    preferred_centre_id: Optional[UUID] = None
    student_notes: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicationSubmitRequest(BaseModel):
    """Schema for submitting an application."""

    confirmation: bool = Field(..., description="Student/Institution confirms submission")
    declaration_accepted: bool = Field(..., description="Student/Institution accepts declaration")

    class Config:
        from_attributes = True


class ApplicationCorrectionRequest(BaseModel):
    """Schema for requesting correction on an application."""

    correction_notes: str = Field(..., min_length=1)
    due_date: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicationRejectRequest(BaseModel):
    """Schema for rejecting an application."""

    rejection_reason: str = Field(..., min_length=1)

    class Config:
        from_attributes = True


class ApplicationApproveRequest(BaseModel):
    """Schema for approving an application."""

    admin_remarks: Optional[str] = None
    allocated_centre_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class ApplicationAdminUpdate(BaseModel):
    """Schema for admin update of limited fields."""

    admin_remarks: Optional[str] = None

    class Config:
        from_attributes = True


class StudentBasicInfo(BaseModel):
    """Basic student info for application responses."""

    id: UUID
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    district: Optional[str] = None

    class Config:
        from_attributes = True


class InstitutionBasicInfo(BaseModel):
    """Basic institution info for application responses."""

    id: UUID
    institution_name: str
    district: Optional[str] = None
    contact_person_name: Optional[str] = None

    class Config:
        from_attributes = True


class ExamSessionBasicInfo(BaseModel):
    """Basic exam session info for application responses."""

    id: UUID
    session_name: str
    year: int

    class Config:
        from_attributes = True


class SubjectBasicInfo(BaseModel):
    """Basic subject info for application responses."""

    id: UUID
    subject_name: str

    class Config:
        from_attributes = True


class GradeLevelBasicInfo(BaseModel):
    """Basic grade level info for application responses."""

    id: UUID
    grade_name: str

    class Config:
        from_attributes = True


class ExamCentreBasicInfo(BaseModel):
    """Basic exam centre info for application responses."""

    id: UUID
    centre_name: str
    district: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicationResponse(BaseModel):
    """Response schema for application details."""

    id: UUID
    application_number: str
    student_id: UUID
    institution_id: Optional[UUID] = None
    exam_session_id: UUID
    subject_id: UUID
    grade_level_id: Optional[UUID] = None
    preferred_centre_id: Optional[UUID] = None
    allocated_centre_id: Optional[UUID] = None
    status: ApplicationStatus
    fee_amount: Optional[Decimal] = None
    admin_remarks: Optional[str] = None
    rejection_reason: Optional[str] = None
    correction_notes: Optional[str] = None
    student_notes: Optional[str] = None
    submitted_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationListItemResponse(BaseModel):
    """Response schema for application list items."""

    id: UUID
    application_number: str
    student_id: UUID
    exam_session_id: UUID
    subject_id: UUID
    status: ApplicationStatus
    fee_amount: Optional[Decimal] = None
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentMetadataResponse(BaseModel):
    """Response schema for document metadata."""

    id: UUID
    document_type: str
    file_name: Optional[str] = None
    file_url: str
    mime_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationDetailResponse(BaseModel):
    """Detailed response schema for application with nested info."""

    id: UUID
    application_number: str
    status: ApplicationStatus
    fee_amount: Optional[Decimal] = None
    student: Optional[StudentBasicInfo] = None
    institution: Optional[InstitutionBasicInfo] = None
    session: Optional[ExamSessionBasicInfo] = None
    subject: Optional[SubjectBasicInfo] = None
    grade_level: Optional[GradeLevelBasicInfo] = None
    preferred_centre: Optional[ExamCentreBasicInfo] = None
    allocated_centre: Optional[ExamCentreBasicInfo] = None
    admin_remarks: Optional[str] = None
    rejection_reason: Optional[str] = None
    correction_notes: Optional[str] = None
    student_notes: Optional[str] = None
    documents: Optional[list[DocumentMetadataResponse]] = None
    submitted_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    """Paginated response for application list."""

    items: list[ApplicationListItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True


class DocumentMetadataCreate(BaseModel):
    """Schema for creating document metadata."""

    document_type: str = Field(..., min_length=1, max_length=120)
    file_name: Optional[str] = Field(None, max_length=255)
    file_url: str = Field(..., max_length=1000)
    mime_type: Optional[str] = Field(None, max_length=120)
    file_size_bytes: Optional[int] = None

    class Config:
        from_attributes = True
