"""Repository for StudentProfile data access."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.student import StudentProfile


class StudentRepository:
    """Repository for StudentProfile model data access."""

    def __init__(self, db: Session):
        self.db = db

    def get_profile_by_user_id(self, user_id: UUID) -> Optional[StudentProfile]:
        """Get student profile by user ID."""
        return self.db.query(StudentProfile).filter(
            StudentProfile.user_id == user_id,
        ).first()

    def get_profile_by_id(self, profile_id: UUID) -> Optional[StudentProfile]:
        """Get student profile by ID."""
        return self.db.query(StudentProfile).filter(
            StudentProfile.id == profile_id,
        ).first()

    def create_student_profile(
        self,
        user_id: UUID,
        date_of_birth: Optional[str] = None,
        gender: Optional[str] = None,
        guardian_name: Optional[str] = None,
        guardian_phone: Optional[str] = None,
        guardian_email: Optional[str] = None,
        address_line_1: Optional[str] = None,
        address_line_2: Optional[str] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        pincode: Optional[str] = None,
    ) -> StudentProfile:
        """Create a new student profile."""
        student_profile = StudentProfile(
            user_id=user_id,
            date_of_birth=date_of_birth,
            gender=gender,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            guardian_email=guardian_email,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            district=district,
            state=state,
            pincode=pincode,
            country="India",
        )
        self.db.add(student_profile)
        self.db.flush()
        return student_profile

    def update_student_profile(self, profile_id: UUID, **kwargs) -> Optional[StudentProfile]:
        """Update student profile fields."""
        profile = self.get_profile_by_id(profile_id)
        if not profile:
            return None

        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        self.db.add(profile)
        self.db.flush()
        return profile

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def flush(self):
        """Flush transaction."""
        self.db.flush()
