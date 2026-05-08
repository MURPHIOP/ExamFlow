from fastapi import APIRouter, Depends

from app.api.deps import (
    get_current_active_user,
    require_admin_or_super_admin,
    require_super_admin,
)
from app.models.user import User
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/protected", tags=["protected-test"])


@router.get("/me", response_model=ApiResponse)
async def get_current_user_protected(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user - accessible to all authenticated users.
    
    This is a test endpoint to verify RBAC is working.
    """
    return ApiResponse(
        success=True,
        message="Current user retrieved",
        data={
            "id": str(current_user.id),
            "full_name": current_user.full_name,
            "role": current_user.role.value,
        },
    )


@router.get("/admin-only", response_model=ApiResponse)
async def admin_only_endpoint(
    current_user: User = Depends(require_admin_or_super_admin),
):
    """
    Admin or Super Admin only endpoint.
    
    This is a test endpoint to verify RBAC is working.
    Students and Institutions will get 403 Forbidden.
    """
    return ApiResponse(
        success=True,
        message="You have admin access",
        data={
            "id": str(current_user.id),
            "full_name": current_user.full_name,
            "role": current_user.role.value,
        },
    )


@router.get("/super-admin-only", response_model=ApiResponse)
async def super_admin_only_endpoint(
    current_user: User = Depends(require_super_admin),
):
    """
    Super Admin only endpoint.
    
    This is a test endpoint to verify RBAC is working.
    Only Super Admin can access this.
    """
    return ApiResponse(
        success=True,
        message="You have super admin access",
        data={
            "id": str(current_user.id),
            "full_name": current_user.full_name,
            "role": current_user.role.value,
        },
    )
