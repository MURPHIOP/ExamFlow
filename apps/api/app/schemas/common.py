from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None
    meta: Any | None = None


class PaginatedMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
