"""Repository for Exam Fee data access."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.exam import ExamFee


class ExamFeeRepository:
    """Repository for ExamFee model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> ExamFee:
        """Create a new exam fee."""
        fee = ExamFee(**kwargs)
        self.db.add(fee)
        self.db.flush()
        return fee

    def get_by_id(self, fee_id: UUID) -> Optional[ExamFee]:
        """Get exam fee by ID."""
        return self.db.query(ExamFee).filter(
            ExamFee.id == fee_id,
        ).first()

    def get_fee_for_session_subject_grade(
        self,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
    ) -> Optional[ExamFee]:
        """Get fee for session + subject + grade combination."""
        query = self.db.query(ExamFee).filter(
            ExamFee.exam_session_id == exam_session_id,
            ExamFee.subject_id == subject_id,
            ExamFee.is_active == True,
        )

        if grade_level_id:
            query = query.filter(ExamFee.grade_level_id == grade_level_id)
        else:
            query = query.filter(ExamFee.grade_level_id.is_(None))

        return query.first()

    def exists_for_session_subject_grade(
        self,
        exam_session_id: UUID,
        subject_id: UUID,
        grade_level_id: Optional[UUID] = None,
        exclude_id: Optional[UUID] = None,
    ) -> bool:
        """Check if fee exists for session + subject + grade."""
        query = self.db.query(ExamFee).filter(
            ExamFee.exam_session_id == exam_session_id,
            ExamFee.subject_id == subject_id,
        )

        if grade_level_id:
            query = query.filter(ExamFee.grade_level_id == grade_level_id)
        else:
            query = query.filter(ExamFee.grade_level_id.is_(None))

        if exclude_id:
            query = query.filter(ExamFee.id != exclude_id)

        return query.first() is not None

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        exam_session_id: Optional[UUID] = None,
        subject_id: Optional[UUID] = None,
        grade_level_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[list[ExamFee], int]:
        """List exam fees with pagination and filters."""
        query = self.db.query(ExamFee)

        if exam_session_id:
            query = query.filter(ExamFee.exam_session_id == exam_session_id)

        if subject_id:
            query = query.filter(ExamFee.subject_id == subject_id)

        if grade_level_id:
            query = query.filter(ExamFee.grade_level_id == grade_level_id)

        if is_active is not None:
            query = query.filter(ExamFee.is_active == is_active)

        total = query.count()
        fees = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return fees, total

    def update(self, fee_id: UUID, **kwargs) -> Optional[ExamFee]:
        """Update exam fee."""
        fee = self.get_by_id(fee_id)
        if not fee:
            return None

        for key, value in kwargs.items():
            if hasattr(fee, key):
                setattr(fee, key, value)

        self.db.add(fee)
        self.db.flush()
        return fee

    def deactivate(self, fee_id: UUID) -> bool:
        """Deactivate exam fee."""
        fee = self.get_by_id(fee_id)
        if not fee:
            return False

        fee.is_active = False
        self.db.add(fee)
        self.db.flush()
        return True

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()
