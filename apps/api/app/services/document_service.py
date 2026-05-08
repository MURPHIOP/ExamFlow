"""Service for document management in applications."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.repositories.application_repository import ApplicationRepository
from app.models.enums import DocumentType


class DocumentService:
    """Service for document metadata management."""

    def __init__(self, db: Session):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.app_repo = ApplicationRepository(db)

    def create_document_metadata(
        self,
        application_id: UUID,
        owner_user_id: UUID,
        document_type: str,
        file_name: Optional[str] = None,
        file_url: str = None,
        mime_type: Optional[str] = None,
        file_size_bytes: Optional[int] = None,
    ) -> dict:
        """Create document metadata for an application."""
        # Validate application exists
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        # Validate document type
        try:
            doc_type_enum = DocumentType[document_type.upper()]
        except KeyError:
            doc_type_enum = DocumentType.OTHER

        try:
            document = self.doc_repo.create_document_metadata(
                owner_user_id=owner_user_id,
                application_id=application_id,
                document_type=doc_type_enum,
                file_name=file_name,
                file_url=file_url,
                mime_type=mime_type,
                file_size_bytes=file_size_bytes,
                storage_provider="local",
            )

            self.doc_repo.commit()

            return self._document_to_dict(document)
        except Exception as e:
            self.db.rollback()
            raise

    def list_documents_for_application(
        self,
        application_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """List documents for an application."""
        # Validate application exists
        application = self.app_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        documents, total = self.doc_repo.list_by_application(
            application_id,
            page=page,
            page_size=page_size,
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return {
            "items": [self._document_to_dict(doc) for doc in documents],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def get_document(self, document_id: UUID) -> dict:
        """Get document details."""
        document = self.doc_repo.get_by_id(document_id)
        if not document:
            raise ValueError("Document not found")

        return self._document_to_dict(document)

    def _document_to_dict(self, document) -> dict:
        """Convert document to dictionary."""
        return {
            "id": document.id,
            "document_type": document.document_type.value if hasattr(document.document_type, 'value') else str(document.document_type),
            "file_name": document.file_name,
            "file_url": document.file_url,
            "mime_type": document.mime_type,
            "file_size_bytes": document.file_size_bytes,
            "status": document.status.value if hasattr(document.status, 'value') else str(document.status),
            "created_at": document.created_at,
        }
