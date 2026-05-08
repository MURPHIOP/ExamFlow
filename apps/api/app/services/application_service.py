"""Service for application workflows."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import ApplicationStatus, UserRole
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.institution_repository import InstitutionRepository
from app.repositories.user_repository import UserRepository
from app.services.application_number_service import ApplicationNumberService
from app.services.application_status_service import ApplicationStatusService
from app.services.application_validation_service import ApplicationValidationService
from app.services.audit_service import AuditService
from app.repositories.exam_fee_repository import ExamFeeRepository
from app.repositories.exam_session_repository import ExamSessionRepository


class ApplicationService:
    """Service for application workflows."""

    def __init__(self, db: Session):
        self.db = db
        self.app_repo = ApplicationRepository(db)
        self.student_repo = StudentRepository(db)
        self.institution_repo = InstitutionRepository(db)
        self.user_repo = UserRepository(db)
        self.number_service = ApplicationNumberService(db)
        self.validation_service = ApplicationValidationService(db)
        self.status_service = ApplicationStatusService()
        self.audit_service = AuditService(db)
        self.fee_repo = ExamFeeRepository(db)
        self.session_repo = ExamSessionRepository(db)

    def create_student_application(
        self,
        student_user: User,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
        preferred_centre_id: Optional[UUID] = None,
        student_notes: Optional[str] = None,
    ) -> dict:
        """Create a draft application for a student."""
        # Validate inputs
        self.validation_service.validate_exam_session(exam_session_id)
        self.validation_service.validate_exam_session_dates(exam_session_id)
        self.validation_service.validate_subject(subject_id)
        self.validation_service.validate_grade_level(grade_level_id)
        self.validation_service.validate_centre(preferred_centre_id)
        self.validation_service.validate_fee_configured(exam_session_id, subject_id, grade_level_id)
        self.validation_service.validate_no_duplicate_active_application(
            student_user.student_profile.id,
            exam_session_id,
            subject_id,
            grade_level_id,
        )

        # Get fee amount
        fee = self.fee_repo.get_fee_for_session_subject_grade(
            exam_session_id,
            subject_id,
            grade_level_id,
        )
        fee_amount = fee.amount if fee else None

        # Get exam session year
        session = self.session_repo.get_by_id(exam_session_id)
        exam_year = session.year if hasattr(session, 'year') else datetime.utcnow().year

        # Generate application number
        app_number = self.number_service.generate_application_number(exam_year)

        try:
            # Create application
            application = self.app_repo.create(
                application_number=app_number,
                student_id=student_user.student_profile.id,
                exam_session_id=exam_session_id,
                subject_id=subject_id,
                fee_amount=fee_amount,
                institution_id=None,
                grade_level_id=grade_level_id,
                preferred_centre_id=preferred_centre_id,
                student_notes=student_notes,
                status=ApplicationStatus.DRAFT,
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_CREATED",
                entity_type="APPLICATION",
                actor_user_id=student_user.id,
                entity_id=application.id,
                metadata={
                    "application_number": app_number,
                    "exam_session_id": str(exam_session_id),
                    "subject_id": str(subject_id),
                },
            )

            self.app_repo.commit()

            return {
                "id": application.id,
                "application_number": application.application_number,
                "status": application.status,
                "fee_amount": str(application.fee_amount),
            }
        except Exception as e:
            self.app_repo.rollback()
            raise

    def create_institution_application(
        self,
        institution_user: User,
        student_user_id: Optional[UUID] = None,
        existing_student_profile_id: Optional[UUID] = None,
        student_data: Optional[dict] = None,
        exam_session_id: UUID = None,
        subject_id: UUID = None,
        grade_level_id: Optional[UUID] = None,
        preferred_centre_id: Optional[UUID] = None,
        institution_notes: Optional[str] = None,
    ) -> dict:
        """Create an application through institution for a student."""
        # Validate institution is approved
        institution = self.institution_repo.ensure_approved_or_allowed(institution_user.id)

        # Get or create student profile
        if student_user_id:
            student_user = self.user_repo.get_by_id(student_user_id)
            if not student_user:
                raise ValueError(f"Student user not found")
            student_profile = student_user.student_profile
        elif existing_student_profile_id:
            student_profile = self.student_repo.get_profile_by_id(existing_student_profile_id)
            if not student_profile:
                raise ValueError("Student profile not found")
            student_user = student_profile.user
        elif student_data:
            # Create new student profile
            # For now, we'll just use the data provided
            # In production, institution would need to match the student
            raise ValueError("Creating new student profiles through institution not yet fully supported")
        else:
            raise ValueError(
                "Must provide either student_user_id, existing_student_profile_id, or student_data"
            )

        # Validate inputs
        self.validation_service.validate_exam_session(exam_session_id)
        self.validation_service.validate_exam_session_dates(exam_session_id)
        self.validation_service.validate_subject(subject_id)
        self.validation_service.validate_grade_level(grade_level_id)
        self.validation_service.validate_centre(preferred_centre_id)
        self.validation_service.validate_fee_configured(exam_session_id, subject_id, grade_level_id)
        self.validation_service.validate_no_duplicate_active_application(
            student_profile.id,
            exam_session_id,
            subject_id,
            grade_level_id,
        )

        # Get fee amount
        fee = self.fee_repo.get_fee_for_session_subject_grade(
            exam_session_id,
            subject_id,
            grade_level_id,
        )
        fee_amount = fee.amount if fee else None

        # Get exam session year
        session = self.session_repo.get_by_id(exam_session_id)
        exam_year = session.year if hasattr(session, 'year') else datetime.utcnow().year

        # Generate application number
        app_number = self.number_service.generate_application_number(exam_year)

        try:
            # Create application
            application = self.app_repo.create(
                application_number=app_number,
                student_id=student_profile.id,
                exam_session_id=exam_session_id,
                subject_id=subject_id,
                fee_amount=fee_amount,
                institution_id=institution.id,
                grade_level_id=grade_level_id,
                preferred_centre_id=preferred_centre_id,
                student_notes=institution_notes,
                status=ApplicationStatus.DRAFT,
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_CREATED",
                entity_type="APPLICATION",
                actor_user_id=institution_user.id,
                entity_id=application.id,
                metadata={
                    "application_number": app_number,
                    "institution_id": str(institution.id),
                    "student_id": str(student_profile.id),
                },
            )

            self.app_repo.commit()

            return {
                "id": application.id,
                "application_number": application.application_number,
                "status": application.status,
                "fee_amount": str(application.fee_amount),
            }
        except Exception as e:
            self.app_repo.rollback()
            raise

    def get_application(self, application_id: UUID) -> dict:
        """Get application details."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        return self._application_to_dict(application)

    def update_student_application(
        self,
        application_id: UUID,
        student_user: User,
        subject_id: Optional[UUID] = None,
        grade_level_id: Optional[UUID] = None,
        preferred_centre_id: Optional[UUID] = None,
        student_notes: Optional[str] = None,
    ) -> dict:
        """Update a student's own application."""
        # Validate ownership and editability
        self.validation_service.validate_application_ownership(
            application_id,
            student_user.student_profile.id,
        )
        self.validation_service.validate_application_editable(application_id)

        application = self.app_repo.get_by_id(application_id)

        # Validate new values if provided
        if subject_id and subject_id != application.subject_id:
            self.validation_service.validate_subject(subject_id)

        if grade_level_id and grade_level_id != application.grade_level_id:
            self.validation_service.validate_grade_level(grade_level_id)

        if preferred_centre_id and preferred_centre_id != application.preferred_centre_id:
            self.validation_service.validate_centre(preferred_centre_id)

        # Recalculate fee if subject/grade changed
        if subject_id or grade_level_id:
            new_subject_id = subject_id or application.subject_id
            new_grade_id = grade_level_id or application.grade_level_id
            fee = self.fee_repo.get_fee_for_session_subject_grade(
                application.exam_session_id,
                new_subject_id,
                new_grade_id,
            )
            if fee:
                application.fee_amount = fee.amount

        try:
            # Update fields
            if subject_id is not None:
                application.subject_id = subject_id
            if grade_level_id is not None:
                application.grade_level_id = grade_level_id
            if preferred_centre_id is not None:
                application.preferred_centre_id = preferred_centre_id
            if student_notes is not None:
                application.student_notes = student_notes

            self.app_repo.update(application_id, **{
                'subject_id': application.subject_id,
                'grade_level_id': application.grade_level_id,
                'preferred_centre_id': application.preferred_centre_id,
                'student_notes': application.student_notes,
                'fee_amount': application.fee_amount,
            })

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_UPDATED",
                entity_type="APPLICATION",
                actor_user_id=student_user.id,
                entity_id=application_id,
                metadata={
                    "application_number": application.application_number,
                },
            )

            self.app_repo.commit()

            return self._application_to_dict(self.app_repo.get_by_id(application_id))
        except Exception as e:
            self.app_repo.rollback()
            raise

    def submit_application(
        self,
        application_id: UUID,
        user: User,
        confirmation: bool = False,
        declaration_accepted: bool = False,
    ) -> dict:
        """Submit an application."""
        if not confirmation or not declaration_accepted:
            raise ValueError("Confirmation and declaration acceptance are required")

        # Validate ownership
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        if application.student_id != user.student_profile.id:
            raise ValueError("You do not have permission to submit this application")

        self.validation_service.validate_application_submittable(application_id)

        try:
            # Determine next status based on fee
            if application.fee_amount and application.fee_amount > 0:
                new_status = ApplicationStatus.PAYMENT_PENDING
            else:
                new_status = ApplicationStatus.SUBMITTED

            # Update status
            application = self.app_repo.update_status(
                application_id,
                new_status,
                submitted_by_user_id=user.id,
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_SUBMITTED",
                entity_type="APPLICATION",
                actor_user_id=user.id,
                entity_id=application_id,
                metadata={
                    "application_number": application.application_number,
                    "new_status": new_status,
                },
            )

            self.app_repo.commit()

            return self._application_to_dict(application)
        except Exception as e:
            self.app_repo.rollback()
            raise

    def list_student_applications(
        self,
        student_user: User,
        page: int = 1,
        page_size: int = 20,
        status: Optional[ApplicationStatus] = None,
        exam_session_id: Optional[UUID] = None,
    ) -> dict:
        """List applications for a student."""
        applications, total = self.app_repo.list_for_student(
            student_user.student_profile.id,
            page=page,
            page_size=page_size,
            status=status,
            exam_session_id=exam_session_id,
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._application_to_list_dict(app) for app in applications],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def list_institution_applications(
        self,
        institution_user: User,
        page: int = 1,
        page_size: int = 20,
        status: Optional[ApplicationStatus] = None,
        exam_session_id: Optional[UUID] = None,
        subject_id: Optional[UUID] = None,
    ) -> dict:
        """List applications for an institution."""
        institution = self.institution_repo.get_by_user_id(institution_user.id)
        if not institution:
            raise ValueError("Institution not found")

        applications, total = self.app_repo.list_for_institution(
            institution.id,
            page=page,
            page_size=page_size,
            status=status,
            exam_session_id=exam_session_id,
            subject_id=subject_id,
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._application_to_list_dict(app) for app in applications],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def list_admin_applications(
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
    ) -> dict:
        """List all applications for admin."""
        applications, total = self.app_repo.list_for_admin(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            exam_session_id=exam_session_id,
            subject_id=subject_id,
            grade_level_id=grade_level_id,
            institution_id=institution_id,
            preferred_centre_id=preferred_centre_id,
            allocated_centre_id=allocated_centre_id,
            district=district,
            date_from=date_from,
            date_to=date_to,
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._application_to_list_dict(app) for app in applications],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def mark_under_verification(
        self,
        application_id: UUID,
        admin_user: User,
    ) -> dict:
        """Mark application as under verification (admin action)."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        # Validate status - can be from submitted, payment_pending, or correction_required
        allowed_from_statuses = [
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.PAYMENT_PENDING,
            ApplicationStatus.CORRECTION_REQUIRED,
        ]

        if application.status not in allowed_from_statuses:
            raise ValueError(
                f"Application cannot be moved to under_verification from {application.status} status"
            )

        try:
            application = self.app_repo.update_status(
                application_id,
                ApplicationStatus.UNDER_VERIFICATION,
                verified_by_user_id=admin_user.id,
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_STATUS_CHANGED",
                entity_type="APPLICATION",
                actor_user_id=admin_user.id,
                entity_id=application_id,
                metadata={
                    "application_number": application.application_number,
                    "from_status": application.status,
                    "to_status": ApplicationStatus.UNDER_VERIFICATION,
                },
            )

            self.app_repo.commit()

            return self._application_to_dict(application)
        except Exception as e:
            self.app_repo.rollback()
            raise

    def request_correction(
        self,
        application_id: UUID,
        admin_user: User,
        correction_notes: str,
        due_date: Optional[str] = None,
    ) -> dict:
        """Request correction for an application (admin action)."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        self.validation_service.validate_application_under_verification(application_id)

        try:
            application = self.app_repo.update(
                application_id,
                status=ApplicationStatus.CORRECTION_REQUIRED,
                correction_notes=correction_notes,
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_CORRECTION_REQUESTED",
                entity_type="APPLICATION",
                actor_user_id=admin_user.id,
                entity_id=application_id,
                metadata={
                    "application_number": application.application_number,
                    "correction_notes": correction_notes,
                },
            )

            self.app_repo.commit()

            return self._application_to_dict(application)
        except Exception as e:
            self.app_repo.rollback()
            raise

    def approve_application(
        self,
        application_id: UUID,
        admin_user: User,
        admin_remarks: Optional[str] = None,
        allocated_centre_id: Optional[UUID] = None,
    ) -> dict:
        """Approve an application (admin action)."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        self.validation_service.validate_application_under_verification(application_id)

        try:
            application = self.app_repo.update(
                application_id,
                status=ApplicationStatus.APPROVED,
                admin_remarks=admin_remarks,
                allocated_centre_id=allocated_centre_id,
                approved_at=datetime.utcnow(),
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_APPROVED",
                entity_type="APPLICATION",
                actor_user_id=admin_user.id,
                entity_id=application_id,
                metadata={
                    "application_number": application.application_number,
                    "admin_remarks": admin_remarks,
                },
            )

            self.app_repo.commit()

            return self._application_to_dict(application)
        except Exception as e:
            self.app_repo.rollback()
            raise

    def reject_application(
        self,
        application_id: UUID,
        admin_user: User,
        rejection_reason: str,
    ) -> dict:
        """Reject an application (admin action)."""
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        # Can reject from under_verification or correction_required
        allowed_from_statuses = [
            ApplicationStatus.UNDER_VERIFICATION,
            ApplicationStatus.CORRECTION_REQUIRED,
        ]

        if application.status not in allowed_from_statuses:
            raise ValueError(
                f"Application cannot be rejected from {application.status} status"
            )

        try:
            application = self.app_repo.update(
                application_id,
                status=ApplicationStatus.REJECTED,
                rejection_reason=rejection_reason,
                rejected_at=datetime.utcnow(),
            )

            # Audit log
            self.audit_service.log_action(
                action="APPLICATION_REJECTED",
                entity_type="APPLICATION",
                actor_user_id=admin_user.id,
                entity_id=application_id,
                metadata={
                    "application_number": application.application_number,
                    "rejection_reason": rejection_reason,
                },
            )

            self.app_repo.commit()

            return self._application_to_dict(application)
        except Exception as e:
            self.app_repo.rollback()
            raise

    def _application_to_dict(self, application) -> dict:
        """Convert application to dictionary."""
        return {
            "id": application.id,
            "application_number": application.application_number,
            "student_id": application.student_id,
            "institution_id": application.institution_id,
            "exam_session_id": application.exam_session_id,
            "subject_id": application.subject_id,
            "grade_level_id": application.grade_level_id,
            "preferred_centre_id": application.preferred_centre_id,
            "allocated_centre_id": application.allocated_centre_id,
            "status": application.status,
            "fee_amount": str(application.fee_amount) if application.fee_amount else None,
            "admin_remarks": application.admin_remarks,
            "rejection_reason": application.rejection_reason,
            "correction_notes": application.correction_notes,
            "student_notes": getattr(application, 'student_notes', None),
            "submitted_at": application.submitted_at,
            "verified_at": application.verified_at,
            "approved_at": application.approved_at,
            "rejected_at": application.rejected_at,
            "created_at": application.created_at,
            "updated_at": application.updated_at,
        }

    def _application_to_list_dict(self, application) -> dict:
        """Convert application to list dictionary."""
        return {
            "id": application.id,
            "application_number": application.application_number,
            "student_id": application.student_id,
            "exam_session_id": application.exam_session_id,
            "subject_id": application.subject_id,
            "status": application.status,
            "fee_amount": str(application.fee_amount) if application.fee_amount else None,
            "submitted_at": application.submitted_at,
            "approved_at": application.approved_at,
            "created_at": application.created_at,
        }
