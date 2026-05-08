from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class RegisterStudentRequest(BaseModel):
    """Schema for student registration."""
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    confirm_password: str
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("email", "phone", mode="before")
    @classmethod
    def check_email_or_phone(cls, v: Optional[str], info) -> Optional[str]:
        # This will be checked after all fields are validated
        return v

    def model_post_init(self, __context) -> None:
        """Validate that at least email or phone is provided."""
        if not self.email and not self.phone:
            raise ValueError("At least email or phone is required")


class RegisterInstitutionRequest(BaseModel):
    """Schema for institution registration."""
    institution_name: str
    contact_person_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str
    confirm_password: str
    registration_number: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    pincode: Optional[str] = None

    @field_validator("institution_name")
    @classmethod
    def validate_institution_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("Institution name must be at least 2 characters")
        return v.strip()

    @field_validator("contact_person_name")
    @classmethod
    def validate_contact_person_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("Contact person name must be at least 2 characters")
        return v.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    def model_post_init(self, __context) -> None:
        """Validate that at least email or phone is provided."""
        if not self.email and not self.phone:
            raise ValueError("At least email or phone is required")


class LoginRequest(BaseModel):
    """Schema for login."""
    identifier: str  # Can be email or phone
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # in seconds


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str


class CurrentUserResponse(BaseModel):
    """Schema for current authenticated user."""
    id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserPublicResponse(BaseModel):
    """Schema for public user information."""
    id: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """Schema for password change."""
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("New password must be at least 8 characters")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v: str, info) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class AuthMessageResponse(BaseModel):
    """Generic auth response message."""
    success: bool
    message: str
    data: dict | None = None
