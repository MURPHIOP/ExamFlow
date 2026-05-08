"""Repository for Grade Level data access."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.exam import GradeLevel


class GradeLevelRepository:
    """Repository for GradeLevel model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> GradeLevel:
        """Create a new grade level."""
        grade_level = GradeLevel(**kwargs)
        self.db.add(grade_level)
        self.db.flush()
        return grade_level

    def get_by_id(self, grade_level_id: UUID) -> Optional[GradeLevel]:
        """Get grade level by ID."""
        return self.db.query(GradeLevel).filter(
            GradeLevel.id == grade_level_id,
            GradeLevel.is_deleted == False,
        ).first()

    def exists_by_subject_and_code(self, subject_id: UUID, code: str, exclude_id: Optional[UUID] = None) -> bool:
        """Check if grade level code exists for subject."""
        query = self.db.query(GradeLevel).filter(
            GradeLevel.subject_id == subject_id,
            GradeLevel.code == code,
            GradeLevel.is_deleted == False,
        )
        if exclude_id:
            query = query.filter(GradeLevel.id != exclude_id)
        return query.first() is not None

    def list_by_subject(
        self,
        subject_id: UUID,
        page: int = 1,
        page_size: int = 100,
        is_active: Optional[bool] = None,
    ) -> tuple[list[GradeLevel], int]:
        """List grade levels for a subject with pagination."""
        query = self.db.query(GradeLevel).filter(
            GradeLevel.subject_id == subject_id,
            GradeLevel.is_deleted == False,
        )

        if is_active is not None:
            query = query.filter(GradeLevel.is_active == is_active)

        query = query.order_by(GradeLevel.display_order)
        
        total = query.count()
        grade_levels = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return grade_levels, total

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        subject_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[list[GradeLevel], int]:
        """List grade levels with pagination and filters."""
        query = self.db.query(GradeLevel).filter(GradeLevel.is_deleted == False)

        if subject_id:
            query = query.filter(GradeLevel.subject_id == subject_id)

        if is_active is not None:
            query = query.filter(GradeLevel.is_active == is_active)

        query = query.order_by(GradeLevel.display_order)
        
        total = query.count()
        grade_levels = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return grade_levels, total

    def update(self, grade_level_id: UUID, **kwargs) -> Optional[GradeLevel]:
        """Update grade level."""
        grade_level = self.get_by_id(grade_level_id)
        if not grade_level:
            return None

        for key, value in kwargs.items():
            if hasattr(grade_level, key):
                setattr(grade_level, key, value)

        self.db.add(grade_level)
        self.db.flush()
        return grade_level

    def soft_delete(self, grade_level_id: UUID) -> bool:
        """Soft delete grade level."""
        grade_level = self.get_by_id(grade_level_id)
        if not grade_level:
            return False

        grade_level.is_deleted = True
        self.db.add(grade_level)
        self.db.flush()
        return True

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()
