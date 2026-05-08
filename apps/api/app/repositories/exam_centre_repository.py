"""Repository for Exam Centre data access."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.centre import ExamCentre


class ExamCentreRepository:
    """Repository for ExamCentre model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> ExamCentre:
        """Create a new exam centre."""
        centre = ExamCentre(**kwargs)
        self.db.add(centre)
        self.db.flush()
        return centre

    def get_by_id(self, centre_id: UUID) -> Optional[ExamCentre]:
        """Get exam centre by ID."""
        return self.db.query(ExamCentre).filter(
            ExamCentre.id == centre_id,
            ExamCentre.is_deleted == False,
        ).first()

    def get_by_code(self, code: str) -> Optional[ExamCentre]:
        """Get exam centre by code."""
        return self.db.query(ExamCentre).filter(
            ExamCentre.code == code,
            ExamCentre.is_deleted == False,
        ).first()

    def exists_by_code(self, code: str, exclude_id: Optional[UUID] = None) -> bool:
        """Check if exam centre code exists."""
        query = self.db.query(ExamCentre).filter(
            ExamCentre.code == code,
            ExamCentre.is_deleted == False,
        )
        if exclude_id:
            query = query.filter(ExamCentre.id != exclude_id)
        return query.first() is not None

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        district: Optional[str] = None,
        status: Optional[str] = None,
    ) -> tuple[list[ExamCentre], int]:
        """List exam centres with pagination and filters."""
        query = self.db.query(ExamCentre).filter(ExamCentre.is_deleted == False)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (ExamCentre.name.ilike(search_term)) | 
                (ExamCentre.code.ilike(search_term)) |
                (ExamCentre.address_line_1.ilike(search_term))
            )

        if district:
            query = query.filter(ExamCentre.district == district)

        if status:
            query = query.filter(ExamCentre.status == status)

        total = query.count()
        centres = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return centres, total

    def list_active_centres(
        self,
        page: int = 1,
        page_size: int = 100,
        district: Optional[str] = None,
    ) -> tuple[list[ExamCentre], int]:
        """List active centres (public)."""
        query = self.db.query(ExamCentre).filter(
            ExamCentre.is_deleted == False,
            ExamCentre.status == "active",
        )

        if district:
            query = query.filter(ExamCentre.district == district)

        total = query.count()
        centres = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return centres, total

    def update(self, centre_id: UUID, **kwargs) -> Optional[ExamCentre]:
        """Update exam centre."""
        centre = self.get_by_id(centre_id)
        if not centre:
            return None

        for key, value in kwargs.items():
            if hasattr(centre, key):
                setattr(centre, key, value)

        self.db.add(centre)
        self.db.flush()
        return centre

    def soft_delete(self, centre_id: UUID) -> bool:
        """Soft delete exam centre."""
        centre = self.get_by_id(centre_id)
        if not centre:
            return False

        centre.is_deleted = True
        self.db.add(centre)
        self.db.flush()
        return True

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()
