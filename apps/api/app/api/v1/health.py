from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    settings = get_settings()
    return {
        "success": True,
        "message": "ExamFlow API is running",
        "service": f"{settings.app_name} by {settings.company_name}",
        "version": "0.1.0",
        "environment": settings.app_env,
    }
