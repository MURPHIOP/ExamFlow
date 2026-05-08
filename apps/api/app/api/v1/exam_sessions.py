"""API routes for Exam Session management."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_super_admin, require_admin_or_super_admin
from app.schemas.common import ApiResponse
from app.schemas.exam_session import (
    ExamSessionCreate,
    ExamSessionUpdate,
    ExamSessionResponse,
    ExamSessionListResponse,
)
from app.services.exam_session_service import ExamSessionService

router = APIRouter(prefix="/exam-sessions", tags=["Exam Sessions"])


@router.get("", response_model=ApiResponse)
async def list_exam_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    current_user=Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """List exam sessions (Admin/Super Admin only)."""
    try:
        service = ExamSessionService(db)
        result = service.list(
            page=page,
            page_size=page_size,
            search=search,
            year=year,
            status=status,
        )
        return ApiResponse(
            success=True,
            message="Exam sessions retrieved successfully",
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active", response_model=ApiResponse)
async def list_active_exam_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List active exam sessions (public)."""
    try:
        service = ExamSessionService(db)
        result = service.list_active(page=page, page_size=page_size)
        return ApiResponse(
            success=True,
            message="Active exam sessions retrieved successfully",
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=ApiResponse)
async def get_exam_session(
    session_id: UUID,
    current_user=Depends(require_admin_or_super_admin),
    db: Session = Depends(get_db),
):
    """Get exam session by ID (Admin/Super Admin only)."""
    try:
        service = ExamSessionService(db)
        result = service.get_by_id(session_id)
        return ApiResponse(
            success=True,
            message="Exam session retrieved successfully",
            data=result,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_session(
    data: ExamSessionCreate,
    current_user=Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    """Create exam session (Super Admin only)."""
    try:
        service = ExamSessionService(db)
        result = service.create(data)
        return ApiResponse(
            success=True,
            message="Exam session created successfully",
            data=result,
        )
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{session_id}", response_model=ApiResponse)
async def update_exam_session(
    session_id: UUID,
    data: ExamSessionUpdate,
    current_user=Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    """Update exam session (Super Admin only)."""
    try:
        service = ExamSessionService(db)
        result = service.update(session_id, data)
        return ApiResponse(
            success=True,
            message="Exam session updated successfully",
            data=result,
        )
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        if "already exists" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}", response_model=ApiResponse)
async def delete_exam_session(
    session_id: UUID,
    current_user=Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    """Delete exam session (Super Admin only, soft delete)."""
    try:
        service = ExamSessionService(db)
        service.delete(session_id)
        return ApiResponse(
            success=True,
            message="Exam session deleted successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
