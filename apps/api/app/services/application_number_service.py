"""Service for generating application numbers."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.application_repository import ApplicationRepository


class ApplicationNumberService:
    """Service for generating unique application numbers."""

    def __init__(self, db: Session):
        self.db = db
        self.app_repo = ApplicationRepository(db)

    def generate_application_number(self, exam_session_year: Optional[int] = None) -> str:
        """
        Generate a unique application number.

        Format: MBT-BSP-{YEAR}-{6_DIGIT_SEQUENCE}

        Uses exam session year if available, otherwise uses current year.
        Ensures uniqueness against database with retry logic.
        """
        if exam_session_year is None:
            exam_session_year = datetime.utcnow().year

        # Try to generate a unique number with retries
        max_retries = 10
        for attempt in range(max_retries):
            # Get current max sequence for this year
            # We'll use a simple approach: count applications for this year
            count_query = self.db.query(ApplicationRepository).filter(
                ApplicationRepository.application_number.ilike(f"MBT-BSP-{exam_session_year}-%")
            ).count()

            sequence = count_query + 1 + attempt

            # Format as 6-digit sequence
            app_number = f"MBT-BSP-{exam_session_year}-{sequence:06d}"

            # Check if this number already exists
            if not self.app_repo.get_by_application_number(app_number):
                return app_number

        raise RuntimeError(f"Could not generate unique application number after {max_retries} attempts")
