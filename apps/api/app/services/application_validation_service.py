"""Service for validating applications."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import ApplicationStatus, ExamSessionStatus
from app.repositories.application_repository import ApplicationRepository
from app.repositories.exam_fee_repository import ExamFeeRepository
from app.repositories.exam_session_repository import ExamSessionRepository
from app.repositories.subject_repository import SubjectRepository
from app.repositories.grade_level_repository import GradeLevelRepository
from app.repositories.exam_centre_repository import ExamCentreRepository


class ApplicationValidationService:
    """Service for validating application data and business rules."""

    def __init__(self, db: Session):
        self.db = db
        self.app_repo = ApplicationRepository(db)
        self.session_repo = ExamSessionRepository(db)
        self.subject_repo = SubjectRepository(db)
        self.grade_repo = GradeLevelRepository(db)
        self.centre_repo = ExamCentreRepository(db)
        self.fee_repo = ExamFeeRepository(db)

    def validate_exam_session(self, exam_session_id: UUID) -> None:
        """Validate that exam session exists and is active."""
        session = self.session_repo.get_by_id(exam_session_id)
        if not session:
            raise ValueError(f"Exam session with ID '{exam_session_id}' not found")

        if session.status != ExamSessionStatus.ACTIVE:
            raise ValueError(f"Exam session is not active. Current status: {session.status}")

    def validate_exam_session_dates(self, exam_session_id: UUID) -> None:
        """Validate that application date falls within session's application window."""
        session = self.session_repo.get_by_id(exam_session_id)
        if not session:
            return  # Already validated in validate_exam_session

        now = datetime.utcnow()

        if hasattr(session, 'application_start_date') and session.application_start_date:
            if now < session.application_start_date:
                raise ValueError("Application window has not started yet")

        if hasattr(session, 'application_end_date') and session.application_end_date:
            if now > session.application_end_date:
                raise ValueError("Application window has closed")

    def validate_subject(self, subject_id: UUID) -> None:
        """Validate that subject exists and is active."""
        subject = self.subject_repo.get_by_id(subject_id)
        if not subject:
            raise ValueError(f"Subject with ID '{subject_id}' not found")

        if not getattr(subject, 'is_active', True):
            raise ValueError(f"Subject '{subject.subject_name}' is inactive")

    def validate_grade_level(self, grade_level_id: UUID) -> None:
        """Validate that grade level exists and is active."""
        if not grade_level_id:
            return

        grade_level = self.grade_repo.get_by_id(grade_level_id)
        if not grade_level:
            raise ValueError(f"Grade level with ID '{grade_level_id}' not found")

        if not getattr(grade_level, 'is_active', True):
            raise ValueError(f"Grade level '{grade_level.grade_name}' is inactive")

    def validate_centre(self, centre_id: UUID) -> None:
        """Validate that exam centre exists and is active."""
        if not centre_id:
            return

        centre = self.centre_repo.get_by_id(centre_id)
        if not centre:
            raise ValueError(f"Exam centre with ID '{centre_id}' not found")

        if not getattr(centre, 'is_active', True):
            raise ValueError(f"Exam centre '{centre.centre_name}' is inactive")

    def validate_fee_configured(
        self,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
    ) -> None:
        """Validate that exam fee is configured for this combination."""
        fee = self.fee_repo.get_fee_for_session_subject_grade(
            exam_session_id,
            subject_id,
            grade_level_id,
        )

        if not fee:
            raise ValueError(
                "Exam fee is not configured for this session/subject/grade combination. "
                "Please contact administrator."
            )

    def validate_no_duplicate_active_application(
        self,
        student_id: UUID,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
        exclude_application_id: Optional[UUID] = None,
    ) -> None:
        """Validate that no active duplicate application exists."""
        if self.app_repo.exists_active_duplicate(
            student_id,
            exam_session_id,
            subject_id,
            grade_level_id,
            exclude_application_id,
        ):
            raise ValueError(
                "An active application already exists for this subject and grade in this exam session"
            )

    def validate_application_ownership(
        self,
        application_id: UUID,
        student_id: UUID,
    ) -> None:
        """Validate that student owns the application."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError(f"Application not found")

        if application.student_id != student_id:
            raise ValueError("You do not have permission to access this application")

    def validate_application_editable(self, application_id: UUID) -> None:
        """Validate that application is in editable status."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        editable_statuses = [
            ApplicationStatus.DRAFT,
            ApplicationStatus.CORRECTION_REQUIRED,
        ]

        if application.status not in editable_statuses:
            raise ValueError(
                f"Application cannot be edited in {application.status} status. "
                f"Editable statuses: {editable_statuses}"
            )

    def validate_application_submittable(self, application_id: UUID) -> None:
        """Validate that application can be submitted."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        submittable_statuses = [
            ApplicationStatus.DRAFT,
            ApplicationStatus.CORRECTION_REQUIRED,
        ]

        if application.status not in submittable_statuses:
            raise ValueError(
                f"Application cannot be submitted from {application.status} status. "
                f"Submittable statuses: {submittable_statuses}"
            )

    def validate_application_under_verification(self, application_id: UUID) -> None:
        """Validate that application is under verification."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        if application.status != ApplicationStatus.UNDER_VERIFICATION:
            raise ValueError(
                f"This action requires application to be under verification. "
                f"Current status: {application.status}"
            )
