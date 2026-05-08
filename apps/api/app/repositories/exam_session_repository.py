"""Repository for Exam Session data access."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.exam import ExamSession


class ExamSessionRepository:
    """Repository for ExamSession model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> ExamSession:
        """Create a new exam session."""
        session = ExamSession(**kwargs)
        self.db.add(session)
        self.db.flush()
        return session

    def get_by_id(self, session_id: UUID) -> Optional[ExamSession]:
        """Get exam session by ID."""
        return self.db.query(ExamSession).filter(
            ExamSession.id == session_id,
            ExamSession.is_deleted == False,
        ).first()

    def get_by_code(self, code: str) -> Optional[ExamSession]:
        """Get exam session by code."""
        return self.db.query(ExamSession).filter(
            ExamSession.code == code,
            ExamSession.is_deleted == False,
        ).first()

    def exists_by_code(self, code: str, exclude_id: Optional[UUID] = None) -> bool:
        """Check if exam session code exists."""
        query = self.db.query(ExamSession).filter(
            ExamSession.code == code,
            ExamSession.is_deleted == False,
        )
        if exclude_id:
            query = query.filter(ExamSession.id != exclude_id)
        return query.first() is not None

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        year: Optional[int] = None,
        status: Optional[str] = None,
    ) -> tuple[list[ExamSession], int]:
        """List exam sessions with pagination and filters."""
        query = self.db.query(ExamSession).filter(ExamSession.is_deleted == False)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (ExamSession.name.ilike(search_term)) | 
                (ExamSession.code.ilike(search_term))
            )

        if year is not None:
            query = query.filter(ExamSession.year == year)

        if status:
            query = query.filter(ExamSession.status == status)

        total = query.count()
        sessions = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return sessions, total

    def update(self, session_id: UUID, **kwargs) -> Optional[ExamSession]:
        """Update exam session."""
        session = self.get_by_id(session_id)
        if not session:
            return None

        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)

        self.db.add(session)
        self.db.flush()
        return session

    def soft_delete(self, session_id: UUID) -> bool:
        """Soft delete exam session."""
        session = self.get_by_id(session_id)
        if not session:
            return False

        session.is_deleted = True
        self.db.add(session)
        self.db.flush()
        return True

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()
