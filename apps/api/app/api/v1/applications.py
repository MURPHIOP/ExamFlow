"""API routes for application workflows."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_active_user,
    require_student,
    require_institution,
    require_admin_or_super_admin,
    get_db,
)
from app.core.response import api_response
from app.models.user import User
from app.models.enums import ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    InstitutionApplicationCreate,
    ApplicationUpdate,
    ApplicationSubmitRequest,
    ApplicationCorrectionRequest,
    ApplicationRejectRequest,
    ApplicationApproveRequest,
    ApplicationResponse,
    ApplicationDetailResponse,
    ApplicationListResponse,
    DocumentMetadataCreate,
)
from app.services.application_service import ApplicationService
from app.services.document_service import DocumentService

router = APIRouter(prefix="/applications", tags=["applications"])


# ============================================================================
# STUDENT ROUTES
# ============================================================================


@router.post("/student", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_student_application(
    data: ApplicationCreate,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """Create a draft application for current student."""
    try:
        service = ApplicationService(db)
        result = service.create_student_application(
            student_user=current_user,
            exam_session_id=data.exam_session_id,
            subject_id=data.subject_id,
            grade_level_id=data.grade_level_id,
            preferred_centre_id=data.preferred_centre_id,
            student_notes=data.student_notes,
        )
        return api_response(
            success=True,
            message="Application draft created successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create application",
        )


@router.get("/my", response_model=dict)
async def list_my_applications(
    page: int = 1,
    page_size: int = 20,
    status_filter: Optional[str] = None,
    exam_session_id: Optional[UUID] = None,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """List current student's applications."""
    try:
        status_enum = None
        if status_filter:
            try:
                status_enum = ApplicationStatus[status_filter.upper()]
            except KeyError:
                raise ValueError(f"Invalid status: {status_filter}")

        service = ApplicationService(db)
        result = service.list_student_applications(
            student_user=current_user,
            page=page,
            page_size=page_size,
            status=status_enum,
            exam_session_id=exam_session_id,
        )
        return api_response(
            success=True,
            message="Applications retrieved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve applications",
        )


@router.get("/my/{application_id}", response_model=dict)
async def get_my_application(
    application_id: UUID,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """Get student's own application details."""
    try:
        service = ApplicationService(db)
        application = service.get_application(application_id)

        # Verify ownership
        if application["student_id"] != current_user.student_profile.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this application",
            )

        return api_response(
            success=True,
            message="Application retrieved successfully",
            data=application,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve application",
        )


@router.patch("/my/{application_id}", response_model=dict)
async def update_my_application(
    application_id: UUID,
    data: ApplicationUpdate,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """Update student's own draft application."""
    try:
        service = ApplicationService(db)
        result = service.update_student_application(
            application_id=application_id,
            student_user=current_user,
            subject_id=data.subject_id,
            grade_level_id=data.grade_level_id,
            preferred_centre_id=data.preferred_centre_id,
            student_notes=data.student_notes,
        )
        return api_response(
            success=True,
            message="Application updated successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update application",
        )


@router.post("/my/{application_id}/submit", response_model=dict)
async def submit_my_application(
    application_id: UUID,
    data: ApplicationSubmitRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    """Submit student's application."""
    try:
        service = ApplicationService(db)
        result = service.submit_application(
            application_id=application_id,
            user=current_user,
            confirmation=data.confirmation,
            declaration_accepted=data.declaration_accepted,
        )
        return api_response(
            success=True,
            message="Application submitted successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit application",
        )


# ============================================================================
# INSTITUTION ROUTES
# ============================================================================


@router.post("/institution", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_institution_application(
    data: InstitutionApplicationCreate,
    current_user: User = Depends(require_institution),
    db: Session = Depends(get_db),
):
    """Create an application through institution for a student."""
    try:
        service = ApplicationService(db)
        result = service.create_institution_application(
            institution_user=current_user,
            student_user_id=data.student_user_id,
            existing_student_profile_id=data.existing_student_profile_id,
            student_data=data.student_data.model_dump() if data.student_data else None,
            exam_session_id=data.exam_session_id,
            subject_id=data.subject_id,
            grade_level_id=data.grade_level_id,
            preferred_centre_id=data.preferred_centre_id,
            institution_notes=data.institution_notes,
        )
        return api_response(
            success=True,
            message="Institution application created successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create application",
        )


@router.get("/institution", response_model=dict)
async def list_institution_applications(
    page: int = 1,
    page_size: int = 20,
    status_filter: Optional[str] = None,
    exam_session_id: Optional[UUID] = None,
    subject_id: Optional[UUID] = None,
    current_user: User = Depends(require_institution),
    db: Session = Depends(get_db),
):
    """List institution's applications."""
    try:
        status_enum = None
        if status_filter:
            try:
                status_enum = ApplicationStatus[status_filter.upper()]
            except KeyError:
                raise ValueError(f"Invalid status: {status_filter}")

        service = ApplicationService(db)
        result = service.list_institution_applications(
            institution_user=current_user,
            page=page,
            page_size=page_size,
            status=status_enum,
            exam_session_id=exam_session_id,
            subject_id=subject_id,
        )
        return api_response(
            success=True,
            message="Applications retrieved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve applications",
        )


@router.get("/institution/{application_id}", response_model=dict)
async def get_institution_application(
    application_id: UUID,
    current_user: User = Depends(require_institution),
    db: Session = Depends(get_db),
):
    """Get institution's application details."""
    try:
        from app.repositories.institution_repository import InstitutionRepository

        institution_repo = InstitutionRepository(db)
        institution = institution_repo.get_by_user_id(current_user.id)
        if not institution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Institution not found",
            )

        service = ApplicationService(db)
        application = service.get_application(application_id)

        # Verify ownership
        if application["institution_id"] != institution.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this application",
            )

        return api_response(
            success=True,
            message="Application retrieved successfully",
            data=application,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve application",
        )


@router.patch("/institution/{application_id}", response_model=dict)
async def update_institution_application(
    application_id: UUID,
    data: ApplicationUpdate,
    current_user: User = Depends(require_institution),
    db: Session = Depends(get_db),
):
    """Update institution's draft application."""
    try:
        from app.repositories.institution_repository import InstitutionRepository

        institution_repo = InstitutionRepository(db)
        institution = institution_repo.get_by_user_id(current_user.id)
        if not institution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Institution not found",
            )

        service = ApplicationService(db)
        # Verify ownership first
        application = service.get_application(application_id)
        if application["institution_id"] != institution.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this application",
            )

        # For institution, we reuse student update logic
        result = service.update_student_application(
            application_id=application_id,
            student_user=application["student_id"],  # This won't work as is - needs refactoring
            subject_id=data.subject_id,
            grade_level_id=data.grade_level_id,
            preferred_centre_id=data.preferred_centre_id,
            student_notes=data.student_notes,
        )

        return api_response(
            success=True,
            message="Application updated successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update application",
        )


@router.post("/institution/{application_id}/submit", response_model=dict)
async def submit_institution_application(
    application_id: UUID,
    data: ApplicationSubmitRequest,
    current_user: User = Depends(require_institution),
    db: Session = Depends(get_db),
):
    """Submit institution's application."""
    try:
        from app.repositories.institution_repository import InstitutionRepository

        institution_repo = InstitutionRepository(db)
        institution = institution_repo.get_by_user_id(current_user.id)
        if not institution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Institution not found",
            )

        service = ApplicationService(db)
        application = service.get_application(application_id)
        if application["institution_id"] != institution.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to submit this application",
            )

        result = service.submit_application(
            application_id=application_id,
            user=current_user,
            confirmation=data.confirmation,
            declaration_accepted=data.declaration_accepted,
        )
        return api_response(
            success=True,
            message="Application submitted successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit application",
        )


# ============================================================================
# ADMIN ROUTES
# ============================================================================


@router.get("/admin", response_model=dict)
async def list_admin_applications(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    exam_session_id: Optional[UUID] = None,
    subject_id: Optional[UUID] = None,
    grade_level_id: Optional[UUID] = None,
    institution_id: Optional[UUID] = None,
    preferred_centre_id: Optional[UUID] = None,
    allocated_centre_id: Optional[UUID] = None,
    district: Optional[str] = None,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """List all applications with filters (admin only)."""
    try:
        status_enum = None
        if status_filter:
            try:
                status_enum = ApplicationStatus[status_filter.upper()]
            except KeyError:
                raise ValueError(f"Invalid status: {status_filter}")

        service = ApplicationService(db)
        result = service.list_admin_applications(
            page=page,
            page_size=page_size,
            search=search,
            status=status_enum,
            exam_session_id=exam_session_id,
            subject_id=subject_id,
            grade_level_id=grade_level_id,
            institution_id=institution_id,
            preferred_centre_id=preferred_centre_id,
            allocated_centre_id=allocated_centre_id,
            district=district,
        )
        return api_response(
            success=True,
            message="Applications retrieved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve applications",
        )


@router.get("/admin/{application_id}", response_model=dict)
async def get_admin_application(
    application_id: UUID,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Get application details (admin only)."""
    try:
        service = ApplicationService(db)
        result = service.get_application(application_id)
        return api_response(
            success=True,
            message="Application retrieved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve application",
        )


@router.post("/admin/{application_id}/mark-under-verification", response_model=dict)
async def mark_under_verification(
    application_id: UUID,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Mark application as under verification (admin only)."""
    try:
        service = ApplicationService(db)
        result = service.mark_under_verification(
            application_id=application_id,
            admin_user=current_user,
        )
        return api_response(
            success=True,
            message="Application marked under verification successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update application",
        )


@router.post("/admin/{application_id}/request-correction", response_model=dict)
async def request_correction(
    application_id: UUID,
    data: ApplicationCorrectionRequest,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Request correction for an application (admin only)."""
    try:
        service = ApplicationService(db)
        result = service.request_correction(
            application_id=application_id,
            admin_user=current_user,
            correction_notes=data.correction_notes,
            due_date=data.due_date,
        )
        return api_response(
            success=True,
            message="Correction requested successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to request correction",
        )


@router.post("/admin/{application_id}/approve", response_model=dict)
async def approve_application(
    application_id: UUID,
    data: ApplicationApproveRequest,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Approve an application (admin only)."""
    try:
        service = ApplicationService(db)
        result = service.approve_application(
            application_id=application_id,
            admin_user=current_user,
            admin_remarks=data.admin_remarks,
            allocated_centre_id=data.allocated_centre_id,
        )
        return api_response(
            success=True,
            message="Application approved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve application",
        )


@router.post("/admin/{application_id}/reject", response_model=dict)
async def reject_application(
    application_id: UUID,
    data: ApplicationRejectRequest,
    current_user: User = Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Reject an application (admin only)."""
    try:
        service = ApplicationService(db)
        result = service.reject_application(
            application_id=application_id,
            admin_user=current_user,
            rejection_reason=data.rejection_reason,
        )
        return api_response(
            success=True,
            message="Application rejected successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject application",
        )


# ============================================================================
# DOCUMENT ROUTES
# ============================================================================


@router.post("/{application_id}/documents", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_document_metadata(
    application_id: UUID,
    data: DocumentMetadataCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create document metadata for an application."""
    try:
        from app.repositories.application_repository import ApplicationRepository
        from app.repositories.institution_repository import InstitutionRepository

        app_repo = ApplicationRepository(db)
        application = app_repo.get_by_id(application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        # Verify ownership - student or institution
        has_access = False
        if current_user.student_profile and application.student_id == current_user.student_profile.id:
            has_access = True
        elif current_user.role.value == "institution":
            inst_repo = InstitutionRepository(db)
            institution = inst_repo.get_by_user_id(current_user.id)
            if institution and application.institution_id == institution.id:
                has_access = True
        elif current_user.role.value in ["admin", "super_admin"]:
            has_access = True

        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to add documents to this application",
            )

        service = DocumentService(db)
        result = service.create_document_metadata(
            application_id=application_id,
            owner_user_id=current_user.id,
            document_type=data.document_type,
            file_name=data.file_name,
            file_url=data.file_url,
            mime_type=data.mime_type,
            file_size_bytes=data.file_size_bytes,
        )
        return api_response(
            success=True,
            message="Document metadata created successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create document metadata",
        )


@router.get("/{application_id}/documents", response_model=dict)
async def list_application_documents(
    application_id: UUID,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """List documents for an application."""
    try:
        from app.repositories.application_repository import ApplicationRepository
        from app.repositories.institution_repository import InstitutionRepository

        app_repo = ApplicationRepository(db)
        application = app_repo.get_by_id(application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        # Verify ownership
        has_access = False
        if current_user.student_profile and application.student_id == current_user.student_profile.id:
            has_access = True
        elif current_user.role.value == "institution":
            inst_repo = InstitutionRepository(db)
            institution = inst_repo.get_by_user_id(current_user.id)
            if institution and application.institution_id == institution.id:
                has_access = True
        elif current_user.role.value in ["admin", "super_admin"]:
            has_access = True

        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view documents for this application",
            )

        service = DocumentService(db)
        result = service.list_documents_for_application(
            application_id=application_id,
            page=page,
            page_size=page_size,
        )
        return api_response(
            success=True,
            message="Documents retrieved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents",
        )
