"""Service for Exam Fee business logic."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.exam_fee_repository import ExamFeeRepository
from app.repositories.exam_session_repository import ExamSessionRepository
from app.repositories.subject_repository import SubjectRepository
from app.repositories.grade_level_repository import GradeLevelRepository
from app.schemas.exam_fee import ExamFeeCreate, ExamFeeUpdate


class ExamFeeService:
    """Service for exam fee management."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ExamFeeRepository(db)
        self.session_repo = ExamSessionRepository(db)
        self.subject_repo = SubjectRepository(db)
        self.grade_level_repo = GradeLevelRepository(db)

    def create(self, data: ExamFeeCreate) -> dict:
        """Create exam fee with validation."""
        # Validate exam session exists
        session = self.session_repo.get_by_id(data.exam_session_id)
        if not session:
            raise ValueError(f"Exam session with ID '{data.exam_session_id}' not found")

        # Validate subject exists
        subject = self.subject_repo.get_by_id(data.subject_id)
        if not subject:
            raise ValueError(f"Subject with ID '{data.subject_id}' not found")

        # Validate grade level exists if provided
        if data.grade_level_id:
            grade_level = self.grade_level_repo.get_by_id(data.grade_level_id)
            if not grade_level:
                raise ValueError(f"Grade level with ID '{data.grade_level_id}' not found")

        # Check for duplicate fee config
        if self.repo.exists_for_session_subject_grade(
            data.exam_session_id, data.subject_id, data.grade_level_id
        ):
            raise ValueError(
                "Fee already exists for this session, subject, and grade combination"
            )

        # Create fee
        fee = self.repo.create(
            exam_session_id=data.exam_session_id,
            subject_id=data.subject_id,
            grade_level_id=data.grade_level_id,
            amount=data.amount,
            currency=data.currency,
            late_fee_amount=data.late_fee_amount,
            is_active=data.is_active,
        )
        self.repo.commit()
        
        return {
            "id": fee.id,
            "exam_session_id": fee.exam_session_id,
            "subject_id": fee.subject_id,
            "grade_level_id": fee.grade_level_id,
            "amount": str(fee.amount),
            "currency": fee.currency,
            "late_fee_amount": str(fee.late_fee_amount),
        }

    def get_by_id(self, fee_id: UUID) -> dict:
        """Get exam fee by ID."""
        fee = self.repo.get_by_id(fee_id)
        if not fee:
            raise ValueError("Exam fee not found")

        return self._to_dict(fee)

    def get_fee_for_application(
        self,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
    ) -> dict:
        """Get applicable fee for application form (public lookup)."""
        fee = self.repo.get_fee_for_session_subject_grade(
            exam_session_id, subject_id, grade_level_id
        )
        if not fee:
            raise ValueError(
                "No active fee found for this session, subject, and grade combination"
            )

        return {
            "id": fee.id,
            "amount": str(fee.amount),
            "currency": fee.currency,
            "late_fee_amount": str(fee.late_fee_amount),
            "exam_session_id": fee.exam_session_id,
            "subject_id": fee.subject_id,
            "grade_level_id": fee.grade_level_id,
        }

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        exam_session_id: Optional[UUID] = None,
        subject_id: Optional[UUID] = None,
        grade_level_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
    ) -> dict:
        """List exam fees."""
        fees, total = self.repo.list(
            page=page,
            page_size=page_size,
            exam_session_id=exam_session_id,
            subject_id=subject_id,
            grade_level_id=grade_level_id,
            is_active=is_active,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(f) for f in fees],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def update(self, fee_id: UUID, data: ExamFeeUpdate) -> dict:
        """Update exam fee."""
        fee = self.repo.get_by_id(fee_id)
        if not fee:
            raise ValueError("Exam fee not found")

        # Update fields
        update_data = data.model_dump(exclude_unset=True)
        fee = self.repo.update(fee_id, **update_data)
        self.repo.commit()

        return self._to_dict(fee)

    def delete(self, fee_id: UUID) -> bool:
        """Deactivate exam fee."""
        fee = self.repo.get_by_id(fee_id)
        if not fee:
            raise ValueError("Exam fee not found")

        self.repo.deactivate(fee_id)
        self.repo.commit()
        return True

    def _to_dict(self, fee) -> dict:
        """Convert fee to dict."""
        return {
            "id": fee.id,
            "exam_session_id": fee.exam_session_id,
            "subject_id": fee.subject_id,
            "grade_level_id": fee.grade_level_id,
            "amount": str(fee.amount),
            "currency": fee.currency,
            "late_fee_amount": str(fee.late_fee_amount),
            "is_active": fee.is_active,
            "created_at": fee.created_at,
            "updated_at": fee.updated_at,
        }
