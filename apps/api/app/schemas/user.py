from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserPublicResponse(BaseModel):
    """Public user information."""
    id: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    """Detailed user information."""
    id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
