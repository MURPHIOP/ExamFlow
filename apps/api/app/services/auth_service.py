from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.institution import Institution
from app.models.student import StudentProfile
from app.models.user import User
from app.models.enums import UserRole, InstitutionStatus
from app.repositories.user_repository import UserRepository


class AuthService:
    """Service for authentication and authorization."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_student(
        self,
        full_name: str,
        password: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        gender: Optional[str] = None,
        guardian_name: Optional[str] = None,
        guardian_phone: Optional[str] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        address: Optional[str] = None,
        pincode: Optional[str] = None,
    ) -> User:
        """
        Register a student user and create student profile.
        
        Raises:
            ValueError: If email or phone already exists
        """
        # Check for duplicates
        if email and self.user_repo.email_exists(email):
            raise ValueError("Email already registered")
        if phone and self.user_repo.phone_exists(phone):
            raise ValueError("Phone already registered")

        # Hash password
        password_hash = hash_password(password)

        # Create user in transaction
        try:
            user = self.user_repo.create_user(
                full_name=full_name,
                email=email,
                phone=phone,
                password_hash=password_hash,
                role=UserRole.STUDENT,
                is_active=True,
                is_verified=False,
            )

            # Create student profile
            student_profile = StudentProfile(
                user_id=user.id,
                date_of_birth=date_of_birth,
                gender=gender,
                guardian_name=guardian_name,
                guardian_phone=guardian_phone,
                district=district,
                state=state,
                address=address,
                pincode=pincode,
            )
            self.db.add(student_profile)
            self.user_repo.commit()
            return user
        except Exception as e:
            self.user_repo.rollback()
            raise e

    def register_institution(
        self,
        institution_name: str,
        contact_person_name: str,
        password: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        registration_number: Optional[str] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        address: Optional[str] = None,
        pincode: Optional[str] = None,
    ) -> User:
        """
        Register an institution user and create institution profile with pending status.
        
        Raises:
            ValueError: If email or phone already exists
        """
        # Check for duplicates
        if email and self.user_repo.email_exists(email):
            raise ValueError("Email already registered")
        if phone and self.user_repo.phone_exists(phone):
            raise ValueError("Phone already registered")

        # Hash password
        password_hash = hash_password(password)

        # Create user in transaction
        try:
            user = self.user_repo.create_user(
                full_name=contact_person_name,
                email=email,
                phone=phone,
                password_hash=password_hash,
                role=UserRole.INSTITUTION,
                is_active=True,
                is_verified=False,
            )

            # Create institution profile with pending status
            institution = Institution(
                user_id=user.id,
                institution_name=institution_name,
                contact_person_name=contact_person_name,
                registration_number=registration_number,
                district=district,
                state=state,
                address=address,
                pincode=pincode,
                status=InstitutionStatus.PENDING,
            )
            self.db.add(institution)
            self.user_repo.commit()
            return user
        except Exception as e:
            self.user_repo.rollback()
            raise e

    def authenticate_user(self, identifier: str, password: str) -> Optional[User]:
        """
        Authenticate user by email/phone and password.
        
        Returns:
            User if authentication succeeds, None otherwise
        """
        user = self.user_repo.get_by_identifier(identifier)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def generate_tokens(self, user: User) -> dict:
        """
        Generate access and refresh tokens for user.
        
        Returns:
            Dictionary with access_token, refresh_token, token_type, expires_in
        """
        access_token = create_access_token(str(user.id), user.role.value)
        refresh_token = create_refresh_token(str(user.id), user.role.value)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 30 * 60,  # in seconds
        }

    def get_current_user_data(self, user_id: str) -> Optional[dict]:
        """Get current user data for response."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        return {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
        }

    def update_last_login(self, user_id: str):
        """Update last login timestamp."""
        self.user_repo.update_last_login(user_id)
        self.user_repo.commit()

    def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> bool:
        """
        Change user password.
        
        Returns:
            True if password changed successfully, False otherwise
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False

        if not verify_password(current_password, user.password_hash):
            return False

        user.password_hash = hash_password(new_password)
        self.user_repo.save(user)
        self.user_repo.commit()
        return True
