"""Service for Exam Session business logic."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.exam_session_repository import ExamSessionRepository
from app.schemas.exam_session import ExamSessionCreate, ExamSessionUpdate


class ExamSessionService:
    """Service for exam session management."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ExamSessionRepository(db)

    def create(self, data: ExamSessionCreate) -> dict:
        """Create exam session with validation."""
        # Check for duplicate code
        if self.repo.exists_by_code(data.code):
            raise ValueError(f"Exam session code '{data.code}' already exists")

        # Create session
        session = self.repo.create(
            name=data.name,
            code=data.code,
            year=data.year,
            description=data.description,
            application_start_date=data.application_start_date,
            application_end_date=data.application_end_date,
            exam_start_date=data.exam_start_date,
            exam_end_date=data.exam_end_date,
            result_publish_date=data.result_publish_date,
            certificate_issue_date=data.certificate_issue_date,
            status=data.status,
        )
        self.repo.commit()
        
        return {
            "id": session.id,
            "name": session.name,
            "code": session.code,
            "year": session.year,
            "status": session.status,
        }

    def get_by_id(self, session_id: UUID) -> dict:
        """Get exam session by ID."""
        session = self.repo.get_by_id(session_id)
        if not session:
            raise ValueError("Exam session not found")

        return self._to_dict(session)

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        year: Optional[int] = None,
        status: Optional[str] = None,
    ) -> dict:
        """List exam sessions."""
        sessions, total = self.repo.list(
            page=page,
            page_size=page_size,
            search=search,
            year=year,
            status=status,
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(s) for s in sessions],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def list_active(self, page: int = 1, page_size: int = 100) -> dict:
        """List active exam sessions (public)."""
        sessions, total = self.repo.list(
            page=page,
            page_size=page_size,
            status="active",
        )

        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._to_dict(s) for s in sessions],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    def update(self, session_id: UUID, data: ExamSessionUpdate) -> dict:
        """Update exam session."""
        session = self.repo.get_by_id(session_id)
        if not session:
            raise ValueError("Exam session not found")

        # Check for duplicate code if code is being updated
        if data.code and data.code != session.code:
            if self.repo.exists_by_code(data.code, exclude_id=session_id):
                raise ValueError(f"Exam session code '{data.code}' already exists")

        # Update fields
        update_data = data.model_dump(exclude_unset=True)
        session = self.repo.update(session_id, **update_data)
        self.repo.commit()

        return self._to_dict(session)

    def delete(self, session_id: UUID) -> bool:
        """Soft delete exam session."""
        session = self.repo.get_by_id(session_id)
        if not session:
            raise ValueError("Exam session not found")

        self.repo.soft_delete(session_id)
        self.repo.commit()
        return True

    def _to_dict(self, session) -> dict:
        """Convert session to dict."""
        return {
            "id": session.id,
            "name": session.name,
            "code": session.code,
            "year": session.year,
            "description": session.description,
            "application_start_date": session.application_start_date,
            "application_end_date": session.application_end_date,
            "exam_start_date": session.exam_start_date,
            "exam_end_date": session.exam_end_date,
            "result_publish_date": session.result_publish_date,
            "certificate_issue_date": session.certificate_issue_date,
            "status": session.status,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }
