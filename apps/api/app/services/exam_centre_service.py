"""Service for Exam Centre business logic."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.exam_centre_repository import ExamCentreRepository
from app.schemas.exam_centre import ExamCentreCreate, ExamCentreUpdate


class ExamCentreService:
    """Service for exam centre management."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ExamCentreRepository(db)

    def create(self, data: ExamCentreCreate) -> dict:
        """Create exam centre with validation."""
        # Check for duplicate code
        if self.repo.exists_by_code(data.code):
            raise ValueError(f"Exam centre code '{data.code}' already exists")

        # Create centre
        centre = self.repo.create(
            name=data.name,
            code=data.code,
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            district=data.district,
            state=data.state,
            pincode=data.pincode,
            contact_person_name=data.contact_person_name,
            contact_person_phone=data.contact_person_phone,
            capacity=data.capacity,
            status=data.status,
            latitude=data.latitude,
            longitude=data.longitude,
        )
        self.repo.commit()
        
        return {
            "id": centre.id,
            "name": centre.name,
            "code": centre.code,
            "status": centre.status,
        }

    def get_by_id(self, centre_id: UUID) -> dict:
        """Get exam centre by ID."""
        centre = self.repo.get_by_id(centre_id)
        if not centre:
            raise ValueError("Exam centre not found")

        return self._to_dict(centre)

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        district: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        """List exam centres."""
        centres, total = self.repo.list(
            page=page,
            page_size=page_size,
            search=search,
            district=district,
            status=status,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(c) for c in centres],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def list_active(
        self,
        page: int = 1,
        page_size: int = 100,
        district: Optional[str] = None,
    ) -> dict:
        """List active exam centres (public)."""
        centres, total = self.repo.list_active_centres(
            page=page,
            page_size=page_size,
            district=district,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(c) for c in centres],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def update(self, centre_id: UUID, data: ExamCentreUpdate) -> dict:
        """Update exam centre."""
        centre = self.repo.get_by_id(centre_id)
        if not centre:
            raise ValueError("Exam centre not found")

        # Check for duplicate code if code is being updated
        if data.code and data.code != centre.code:
            if self.repo.exists_by_code(data.code, exclude_id=centre_id):
                raise ValueError(f"Exam centre code '{data.code}' already exists")

        # Update fields
        update_data = data.model_dump(exclude_unset=True)
        centre = self.repo.update(centre_id, **update_data)
        self.repo.commit()

        return self._to_dict(centre)

    def delete(self, centre_id: UUID) -> bool:
        """Soft delete exam centre."""
        centre = self.repo.get_by_id(centre_id)
        if not centre:
            raise ValueError("Exam centre not found")

        self.repo.soft_delete(centre_id)
        self.repo.commit()
        return True

    def _to_dict(self, centre) -> dict:
        """Convert centre to dict."""
        return {
            "id": centre.id,
            "name": centre.name,
            "code": centre.code,
            "address_line_1": centre.address_line_1,
            "address_line_2": centre.address_line_2,
            "district": centre.district,
            "state": centre.state,
            "pincode": centre.pincode,
            "contact_person_name": centre.contact_person_name,
            "contact_person_phone": centre.contact_person_phone,
            "capacity": centre.capacity,
            "status": centre.status,
            "latitude": centre.latitude,
            "longitude": centre.longitude,
            "created_at": centre.created_at,
            "updated_at": centre.updated_at,
        }
