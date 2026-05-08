"""Repository for Subject data access."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.exam import Subject


class SubjectRepository:
    """Repository for Subject model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Subject:
        """Create a new subject."""
        subject = Subject(**kwargs)
        self.db.add(subject)
        self.db.flush()
        return subject

    def get_by_id(self, subject_id: UUID) -> Optional[Subject]:
        """Get subject by ID."""
        return self.db.query(Subject).filter(
            Subject.id == subject_id,
            Subject.is_deleted == False,
        ).first()

    def get_by_code(self, code: str) -> Optional[Subject]:
        """Get subject by code."""
        return self.db.query(Subject).filter(
            Subject.code == code,
            Subject.is_deleted == False,
        ).first()

    def exists_by_code(self, code: str, exclude_id: Optional[UUID] = None) -> bool:
        """Check if subject code exists."""
        query = self.db.query(Subject).filter(
            Subject.code == code,
            Subject.is_deleted == False,
        )
        if exclude_id:
            query = query.filter(Subject.id != exclude_id)
        return query.first() is not None

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[list[Subject], int]:
        """List subjects with pagination and filters."""
        query = self.db.query(Subject).filter(Subject.is_deleted == False)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Subject.name.ilike(search_term)) | 
                (Subject.code.ilike(search_term))
            )

        if category:
            query = query.filter(Subject.category == category)

        if is_active is not None:
            query = query.filter(Subject.is_active == is_active)

        total = query.count()
        subjects = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return subjects, total

    def list_active(
        self,
        page: int = 1,
        page_size: int = 100,
    ) -> tuple[list[Subject], int]:
        """List active subjects only (public)."""
        query = self.db.query(Subject).filter(
            Subject.is_deleted == False,
            Subject.is_active == True,
        )

        total = query.count()
        subjects = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return subjects, total

    def update(self, subject_id: UUID, **kwargs) -> Optional[Subject]:
        """Update subject."""
        subject = self.get_by_id(subject_id)
        if not subject:
            return None

        for key, value in kwargs.items():
            if hasattr(subject, key):
                setattr(subject, key, value)

        self.db.add(subject)
        self.db.flush()
        return subject

    def soft_delete(self, subject_id: UUID) -> bool:
        """Soft delete subject."""
        subject = self.get_by_id(subject_id)
        if not subject:
            return False

        subject.is_deleted = True
        self.db.add(subject)
        self.db.flush()
        return True

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()
