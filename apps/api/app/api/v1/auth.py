from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_active_user,
    get_db,
)
from app.models.user import User
from app.schemas.auth import (
    AuthMessageResponse,
    CurrentUserResponse,
    LoginRequest,
    RegisterInstitutionRequest,
    RegisterStudentRequest,
    TokenResponse,
)
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register/student",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_student(
    request: RegisterStudentRequest,
    req: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new student user.
    
    Creates both User and StudentProfile records.
    """
    try:
        auth_service = AuthService(db)
        audit_service = AuditService(db)

        user = auth_service.register_student(
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            password=request.password,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            guardian_name=request.guardian_name,
            guardian_phone=request.guardian_phone,
            district=request.district,
            state=request.state,
            address=request.address,
            pincode=request.pincode,
        )

        # Log registration
        audit_service.log_user_registered(
            user_id=str(user.id),
            role="STUDENT",
            identifier=request.email or request.phone,
        )

        return ApiResponse(
            success=True,
            message="Student registered successfully",
            data={
                "user_id": str(user.id),
                "email": user.email,
                "phone": user.phone,
            },
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed",
        )


@router.post(
    "/register/institution",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_institution(
    request: RegisterInstitutionRequest,
    req: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new institution user.
    
    Creates both User and Institution records with pending status.
    """
    try:
        auth_service = AuthService(db)
        audit_service = AuditService(db)

        user = auth_service.register_institution(
            institution_name=request.institution_name,
            contact_person_name=request.contact_person_name,
            email=request.email,
            phone=request.phone,
            password=request.password,
            registration_number=request.registration_number,
            district=request.district,
            state=request.state,
            address=request.address,
            pincode=request.pincode,
        )

        # Log registration
        audit_service.log_user_registered(
            user_id=str(user.id),
            role="INSTITUTION",
            identifier=request.email or request.phone,
        )

        return ApiResponse(
            success=True,
            message="Institution registered successfully. Awaiting approval.",
            data={
                "user_id": str(user.id),
                "email": user.email,
                "phone": user.phone,
                "institution_name": request.institution_name,
            },
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed",
        )


@router.post("/login", response_model=ApiResponse)
async def login(
    request: LoginRequest,
    req: Request,
    db: Session = Depends(get_db),
):
    """
    Login with email or phone and password.
    
    Returns JWT access and refresh tokens.
    """
    auth_service = AuthService(db)
    audit_service = AuditService(db)
    client_ip = req.client.host if req.client else None

    user = auth_service.authenticate_user(request.identifier, request.password)

    if not user:
        # Log failed login attempt without exposing if user exists
        audit_service.log_login_failed(request.identifier, client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Update last login
    auth_service.update_last_login(str(user.id))

    # Generate tokens
    tokens = auth_service.generate_tokens(user)

    # Log successful login
    audit_service.log_login_success(str(user.id), client_ip)

    user_data = auth_service.get_current_user_data(str(user.id))

    return ApiResponse(
        success=True,
        message="Login successful",
        data={
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": tokens["token_type"],
            "expires_in": tokens["expires_in"],
            "user": user_data,
        },
    )


@router.get("/me", response_model=ApiResponse)
async def get_current_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current authenticated user information."""
    auth_service = AuthService(db)
    user_data = auth_service.get_current_user_data(str(current_user.id))

    return ApiResponse(
        success=True,
        message="Current user retrieved",
        data=user_data,
    )


@router.post("/logout", response_model=ApiResponse)
async def logout(
    current_user: User = Depends(get_current_active_user),
):
    """
    Logout user.
    
    For JWT-only MVP, client should delete the token from local storage.
    Server-side token invalidation is intentionally not implemented.
    """
    return ApiResponse(
        success=True,
        message="Logout successful. Please delete the token from client storage.",
    )
