"""Service for Grade Level business logic."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.grade_level_repository import GradeLevelRepository
from app.repositories.subject_repository import SubjectRepository
from app.schemas.grade_level import GradeLevelCreate, GradeLevelUpdate


class GradeLevelService:
    """Service for grade level management."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = GradeLevelRepository(db)
        self.subject_repo = SubjectRepository(db)

    def create(self, data: GradeLevelCreate) -> dict:
        """Create grade level with validation."""
        # Validate subject exists
        subject = self.subject_repo.get_by_id(data.subject_id)
        if not subject:
            raise ValueError(f"Subject with ID '{data.subject_id}' not found")

        # Check for duplicate code for this subject
        if self.repo.exists_by_subject_and_code(data.subject_id, data.code):
            raise ValueError(
                f"Grade level code '{data.code}' already exists for this subject"
            )

        # Create grade level
        grade_level = self.repo.create(
            subject_id=data.subject_id,
            name=data.name,
            code=data.code,
            display_order=data.display_order,
            default_fee=data.default_fee,
            is_active=data.is_active,
        )
        self.repo.commit()
        
        return {
            "id": grade_level.id,
            "subject_id": grade_level.subject_id,
            "name": grade_level.name,
            "code": grade_level.code,
            "is_active": grade_level.is_active,
        }

    def get_by_id(self, grade_level_id: UUID) -> dict:
        """Get grade level by ID."""
        grade_level = self.repo.get_by_id(grade_level_id)
        if not grade_level:
            raise ValueError("Grade level not found")

        return self._to_dict(grade_level)

    def list_by_subject(
        self,
        subject_id: UUID,
        page: int = 1,
        page_size: int = 100,
        is_active: Optional[bool] = None,
    ) -> dict:
        """List grade levels for a subject."""
        # Validate subject exists
        subject = self.subject_repo.get_by_id(subject_id)
        if not subject:
            raise ValueError(f"Subject with ID '{subject_id}' not found")

        grade_levels, total = self.repo.list_by_subject(
            subject_id=subject_id,
            page=page,
            page_size=page_size,
            is_active=is_active,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(gl) for gl in grade_levels],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        subject_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
    ) -> dict:
        """List grade levels."""
        grade_levels, total = self.repo.list(
            page=page,
            page_size=page_size,
            subject_id=subject_id,
            is_active=is_active,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(gl) for gl in grade_levels],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def update(self, grade_level_id: UUID, data: GradeLevelUpdate) -> dict:
        """Update grade level."""
        grade_level = self.repo.get_by_id(grade_level_id)
        if not grade_level:
            raise ValueError("Grade level not found")

        # Check for duplicate code if code is being updated
        if data.code and data.code != grade_level.code:
            if self.repo.exists_by_subject_and_code(
                grade_level.subject_id, data.code, exclude_id=grade_level_id
            ):
                raise ValueError(
                    f"Grade level code '{data.code}' already exists for this subject"
                )

        # Update fields
        update_data = data.model_dump(exclude_unset=True)
        grade_level = self.repo.update(grade_level_id, **update_data)
        self.repo.commit()

        return self._to_dict(grade_level)

    def delete(self, grade_level_id: UUID) -> bool:
        """Soft delete grade level."""
        grade_level = self.repo.get_by_id(grade_level_id)
        if not grade_level:
            raise ValueError("Grade level not found")

        self.repo.soft_delete(grade_level_id)
        self.repo.commit()
        return True

    def _to_dict(self, grade_level) -> dict:
        """Convert grade level to dict."""
        return {
            "id": grade_level.id,
            "subject_id": grade_level.subject_id,
            "name": grade_level.name,
            "code": grade_level.code,
            "display_order": grade_level.display_order,
            "default_fee": grade_level.default_fee,
            "is_active": grade_level.is_active,
            "created_at": grade_level.created_at,
            "updated_at": grade_level.updated_at,
        }
