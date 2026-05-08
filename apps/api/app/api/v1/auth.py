import traceback
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.auth import LoginRequest, RegisterStudentRequest
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/student", response_model=ApiResponse, status_code=201)
async def register_student(request: RegisterStudentRequest, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        audit_service = AuditService(db)

        user = auth_service.register_student(
            full_name=request.full_name, email=request.email,
            phone=request.phone, password=request.password,
            date_of_birth=request.date_of_birth, gender=request.gender,
            guardian_name=request.guardian_name, guardian_phone=request.guardian_phone,
            district=request.district, state=request.state,
            address=request.address, pincode=request.pincode
        )

        audit_service.log_user_registered(str(user.id), "STUDENT", request.email or request.phone)

        return ApiResponse(success=True, message="Registered successfully", 
                           data={"user_id": str(user.id)})
    except Exception as e:
        traceback.print_exc() # Prints real error to Uvicorn terminal
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=ApiResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(request.identifier, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    tokens = auth_service.generate_tokens(user)
    return ApiResponse(success=True, message="Login successful", data=tokens)