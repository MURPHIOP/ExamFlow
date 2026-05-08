"""Repository for Institution data access."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.institution import Institution
from app.models.enums import InstitutionStatus


class InstitutionRepository:
    """Repository for Institution model data access."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: UUID) -> Optional[Institution]:
        """Get institution by user ID."""
        return self.db.query(Institution).filter(
            Institution.user_id == user_id,
        ).first()

    def get_by_id(self, institution_id: UUID) -> Optional[Institution]:
        """Get institution by ID."""
        return self.db.query(Institution).filter(
            Institution.id == institution_id,
        ).first()

    def get_approved_by_user_id(self, user_id: UUID) -> Optional[Institution]:
        """Get approved institution by user ID."""
        return self.db.query(Institution).filter(
            Institution.user_id == user_id,
            Institution.status == InstitutionStatus.APPROVED,
        ).first()

    def ensure_approved_or_allowed(self, user_id: UUID) -> Optional[Institution]:
        """Get institution and ensure it's approved for operations."""
        institution = self.get_by_user_id(user_id)
        if not institution:
            return None

        # Only approved institutions can submit applications
        if institution.status != InstitutionStatus.APPROVED:
            raise ValueError(f"Institution is not approved. Current status: {institution.status}")

        return institution

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def flush(self):
        """Flush transaction."""
        self.db.flush()
