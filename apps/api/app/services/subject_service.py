"""Service for Subject business logic."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.subject_repository import SubjectRepository
from app.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectService:
    """Service for subject management."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = SubjectRepository(db)

    def create(self, data: SubjectCreate) -> dict:
        """Create subject with validation."""
        # Check for duplicate code
        if self.repo.exists_by_code(data.code):
            raise ValueError(f"Subject code '{data.code}' already exists")

        # Create subject
        subject = self.repo.create(
            name=data.name,
            code=data.code,
            category=data.category,
            description=data.description,
            is_active=data.is_active,
        )
        self.repo.commit()
        
        return {
            "id": subject.id,
            "name": subject.name,
            "code": subject.code,
            "is_active": subject.is_active,
        }

    def get_by_id(self, subject_id: UUID) -> dict:
        """Get subject by ID."""
        subject = self.repo.get_by_id(subject_id)
        if not subject:
            raise ValueError("Subject not found")

        return self._to_dict(subject)

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> dict:
        """List subjects."""
        subjects, total = self.repo.list(
            page=page,
            page_size=page_size,
            search=search,
            category=category,
            is_active=is_active,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(s) for s in subjects],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def list_active(self, page: int = 1, page_size: int = 100) -> dict:
        """List active subjects (public)."""
        subjects, total = self.repo.list_active(
            page=page,
            page_size=page_size,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(s) for s in subjects],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def update(self, subject_id: UUID, data: SubjectUpdate) -> dict:
        """Update subject."""
        subject = self.repo.get_by_id(subject_id)
        if not subject:
            raise ValueError("Subject not found")

        # Check for duplicate code if code is being updated
        if data.code and data.code != subject.code:
            if self.repo.exists_by_code(data.code, exclude_id=subject_id):
                raise ValueError(f"Subject code '{data.code}' already exists")

        # Update fields
        update_data = data.model_dump(exclude_unset=True)
        subject = self.repo.update(subject_id, **update_data)
        self.repo.commit()

        return self._to_dict(subject)

    def delete(self, subject_id: UUID) -> bool:
        """Soft delete subject."""
        subject = self.repo.get_by_id(subject_id)
        if not subject:
            raise ValueError("Subject not found")

        self.repo.soft_delete(subject_id)
        self.repo.commit()
        return True

    def _to_dict(self, subject) -> dict:
        """Convert subject to dict."""
        return {
            "id": subject.id,
            "name": subject.name,
            "code": subject.code,
            "category": subject.category,
            "description": subject.description,
            "is_active": subject.is_active,
            "created_at": subject.created_at,
            "updated_at": subject.updated_at,
        }
