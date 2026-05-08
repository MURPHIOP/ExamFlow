"""Repository for Application data access."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.enums import ApplicationStatus


class ApplicationRepository:
    """Repository for Application model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        application_number: str,
        student_id: UUID,
        exam_session_id: UUID,
        subject_id: UUID,
        fee_amount=None,
        institution_id: Optional[UUID] = None,
        grade_level_id: Optional[UUID] = None,
        preferred_centre_id: Optional[UUID] = None,
        student_notes: Optional[str] = None,
        status: ApplicationStatus = ApplicationStatus.DRAFT,
    ) -> Application:
        """Create a new application."""
        application = Application(
            application_number=application_number,
            student_id=student_id,
            exam_session_id=exam_session_id,
            subject_id=subject_id,
            institution_id=institution_id,
            grade_level_id=grade_level_id,
            preferred_centre_id=preferred_centre_id,
            fee_amount=fee_amount,
            student_notes=student_notes,
            status=status,
        )
        self.db.add(application)
        self.db.flush()
        return application

    def get_by_id(self, application_id: UUID) -> Optional[Application]:
        """Get application by ID."""
        return self.db.query(Application).filter(
            Application.id == application_id,
            Application.deleted_at.is_(None),
        ).first()

    def get_by_application_number(self, application_number: str) -> Optional[Application]:
        """Get application by application number."""
        return self.db.query(Application).filter(
            Application.application_number == application_number,
            Application.deleted_at.is_(None),
        ).first()

    def list_for_student(
        self,
        student_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[ApplicationStatus] = None,
        exam_session_id: Optional[UUID] = None,
    ) -> tuple[list[Application], int]:
        """List applications for a student."""
        query = self.db.query(Application).filter(
            Application.student_id == student_id,
            Application.deleted_at.is_(None),
        )

        if status:
            query = query.filter(Application.status == status)

        if exam_session_id:
            query = query.filter(Application.exam_session_id == exam_session_id)

        total = query.count()
        offset = (page - 1) * page_size

        applications = query.order_by(Application.created_at.desc()).offset(offset).limit(page_size).all()

        return applications, total

    def list_for_institution(
        self,
        institution_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[ApplicationStatus] = None,
        exam_session_id: Optional[UUID] = None,
        subject_id: Optional[UUID] = None,
    ) -> tuple[list[Application], int]:
        """List applications for an institution."""
        query = self.db.query(Application).filter(
            Application.institution_id == institution_id,
            Application.deleted_at.is_(None),
        )

        if status:
            query = query.filter(Application.status == status)

        if exam_session_id:
            query = query.filter(Application.exam_session_id == exam_session_id)

        if subject_id:
            query = query.filter(Application.subject_id == subject_id)

        total = query.count()
        offset = (page - 1) * page_size

        applications = query.order_by(Application.created_at.desc()).offset(offset).limit(page_size).all()

        return applications, total

    def list_for_admin(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[ApplicationStatus] = None,
        exam_session_id: Optional[UUID] = None,
        subject_id: Optional[UUID] = None,
        grade_level_id: Optional[UUID] = None,
        institution_id: Optional[UUID] = None,
        preferred_centre_id: Optional[UUID] = None,
        allocated_centre_id: Optional[UUID] = None,
        district: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> tuple[list[Application], int]:
        """List applications for admin with advanced filters."""
        query = self.db.query(Application).filter(
            Application.deleted_at.is_(None),
        )

        if search:
            search_term = f"%{search}%"
            # Search by application number (simple for now)
            query = query.filter(
                Application.application_number.ilike(search_term),
            )

        if status:
            query = query.filter(Application.status == status)

        if exam_session_id:
            query = query.filter(Application.exam_session_id == exam_session_id)

        if subject_id:
            query = query.filter(Application.subject_id == subject_id)

        if grade_level_id:
            query = query.filter(Application.grade_level_id == grade_level_id)

        if institution_id:
            query = query.filter(Application.institution_id == institution_id)

        if preferred_centre_id:
            query = query.filter(Application.preferred_centre_id == preferred_centre_id)

        if allocated_centre_id:
            query = query.filter(Application.allocated_centre_id == allocated_centre_id)

        if district:
            # Filter by student's district
            query = query.join(Application.student).filter(
                Application.student.has(StudentProfile.district == district)
            )

        if date_from:
            query = query.filter(Application.created_at >= date_from)

        if date_to:
            query = query.filter(Application.created_at <= date_to)

        total = query.count()
        offset = (page - 1) * page_size

        applications = query.order_by(Application.created_at.desc()).offset(offset).limit(page_size).all()

        return applications, total

    def update(self, application_id: UUID, **kwargs) -> Optional[Application]:
        """Update application fields."""
        application = self.get_by_id(application_id)
        if not application:
            return None

        for key, value in kwargs.items():
            if hasattr(application, key):
                setattr(application, key, value)

        self.db.add(application)
        self.db.flush()
        return application

    def update_status(
        self,
        application_id: UUID,
        new_status: ApplicationStatus,
        submitted_by_user_id: Optional[UUID] = None,
        verified_by_user_id: Optional[UUID] = None,
    ) -> Optional[Application]:
        """Update application status with timestamp tracking."""
        application = self.get_by_id(application_id)
        if not application:
            return None

        application.status = new_status

        if new_status == ApplicationStatus.SUBMITTED:
            application.submitted_at = datetime.utcnow()
            if submitted_by_user_id:
                application.submitted_by_user_id = submitted_by_user_id

        elif new_status == ApplicationStatus.UNDER_VERIFICATION:
            application.verified_at = datetime.utcnow()
            if verified_by_user_id:
                application.verified_by_user_id = verified_by_user_id

        elif new_status == ApplicationStatus.APPROVED:
            application.approved_at = datetime.utcnow()

        elif new_status == ApplicationStatus.REJECTED:
            application.rejected_at = datetime.utcnow()

        self.db.add(application)
        self.db.flush()
        return application

    def exists_active_duplicate(
        self,
        student_id: UUID,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
        exclude_application_id: Optional[UUID] = None,
    ) -> bool:
        """Check if active application exists for this student/session/subject/grade."""
        # Active statuses are those not yet completed
        active_statuses = [
            ApplicationStatus.DRAFT,
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.PAYMENT_PENDING,
            ApplicationStatus.UNDER_VERIFICATION,
            ApplicationStatus.CORRECTION_REQUIRED,
            ApplicationStatus.APPROVED,
        ]

        query = self.db.query(Application).filter(
            Application.student_id == student_id,
            Application.exam_session_id == exam_session_id,
            Application.subject_id == subject_id,
            Application.status.in_(active_statuses),
            Application.deleted_at.is_(None),
        )

        if grade_level_id:
            query = query.filter(Application.grade_level_id == grade_level_id)
        else:
            query = query.filter(Application.grade_level_id.is_(None))

        if exclude_application_id:
            query = query.filter(Application.id != exclude_application_id)

        return query.first() is not None

    def count_by_filters(
        self,
        exam_session_id: Optional[UUID] = None,
        subject_id: Optional[UUID] = None,
        status: Optional[ApplicationStatus] = None,
    ) -> int:
        """Count applications matching filters."""
        query = self.db.query(Application).filter(
            Application.deleted_at.is_(None),
        )

        if exam_session_id:
            query = query.filter(Application.exam_session_id == exam_session_id)

        if subject_id:
            query = query.filter(Application.subject_id == subject_id)

        if status:
            query = query.filter(Application.status == status)

        return query.count()

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def flush(self):
        """Flush transaction."""
        self.db.flush()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()


# Import after class definition to avoid circular imports
from app.models.student import StudentProfile
