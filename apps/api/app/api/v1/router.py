from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.protected_test import router as protected_test_router
from app.api.v1.exam_sessions import router as exam_sessions_router
from app.api.v1.applications import router as applications_router
from app.api.v1.payments import router as payments_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(protected_test_router)
api_v1_router.include_router(exam_sessions_router)
api_v1_router.include_router(applications_router)
api_v1_router.include_router(payments_router)
