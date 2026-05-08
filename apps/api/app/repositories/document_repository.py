"""Repository for Document data access."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.enums import DocumentStatus, DocumentType


class DocumentRepository:
    """Repository for Document model data access."""

    def __init__(self, db: Session):
        self.db = db

    def create_document_metadata(
        self,
        owner_user_id: Optional[UUID] = None,
        application_id: Optional[UUID] = None,
        document_type: DocumentType = DocumentType.OTHER,
        file_name: Optional[str] = None,
        file_url: str = None,
        mime_type: Optional[str] = None,
        file_size_bytes: Optional[int] = None,
        storage_provider: str = "local",
    ) -> Document:
        """Create document metadata."""
        document = Document(
            owner_user_id=owner_user_id,
            application_id=application_id,
            document_type=document_type,
            file_name=file_name,
            file_url=file_url,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            storage_provider=storage_provider,
            status=DocumentStatus.UPLOADED,
        )
        self.db.add(document)
        self.db.flush()
        return document

    def get_by_id(self, document_id: UUID) -> Optional[Document]:
        """Get document by ID."""
        return self.db.query(Document).filter(
            Document.id == document_id,
            Document.deleted_at.is_(None),
        ).first()

    def list_by_application(
        self,
        application_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Document], int]:
        """List documents for an application."""
        query = self.db.query(Document).filter(
            Document.application_id == application_id,
            Document.deleted_at.is_(None),
        )

        total = query.count()
        offset = (page - 1) * page_size

        documents = query.order_by(Document.created_at.desc()).offset(offset).limit(page_size).all()

        return documents, total

    def update_status(
        self,
        document_id: UUID,
        status: DocumentStatus,
        verified_by_user_id: Optional[UUID] = None,
        rejection_reason: Optional[str] = None,
    ) -> Optional[Document]:
        """Update document status."""
        document = self.get_by_id(document_id)
        if not document:
            return None

        document.status = status
        if verified_by_user_id:
            document.verified_by_user_id = verified_by_user_id
        if rejection_reason:
            document.rejection_reason = rejection_reason

        self.db.add(document)
        self.db.flush()
        return document

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def flush(self):
        """Flush transaction."""
        self.db.flush()
