from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "ExamFlow API is running",
        "service": "ExamFlow by M.B. Technosoft Pvt Ltd",
        "version": "0.1.0",
        "environment": settings.app_env,
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "message": "ExamFlow API is running",
        "service": "ExamFlow by M.B. Technosoft Pvt Ltd",
        "version": "0.1.0",
        "environment": settings.app_env,
    }

app.include_router(api_v1_router, prefix="/api/v1")
