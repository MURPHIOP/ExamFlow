from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import CertificateStatus

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.document import Document
    from app.models.result import Result
    from app.models.user import User


class Certificate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "certificates"
    __table_args__ = (
        Index("ix_certificates_certificate_number", "certificate_number"),
        Index("ix_certificates_qr_code_value", "qr_code_value"),
        Index("ix_certificates_status", "status"),
        Index("ix_certificates_issued_at", "issued_at"),
    )

    application_id: Mapped[UUID] = mapped_column(ForeignKey("applications.id"), nullable=False, unique=True)
    result_id: Mapped[UUID | None] = mapped_column(ForeignKey("results.id"), nullable=True)
    certificate_number: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    status: Mapped[CertificateStatus] = mapped_column(
        Enum(CertificateStatus, name="certificate_status"),
        nullable=False,
        server_default=CertificateStatus.PENDING.value,
    )
    pdf_document_id: Mapped[UUID | None] = mapped_column(ForeignKey("documents.id"), nullable=True)
    qr_code_value: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    verification_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    issued_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_by_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoke_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    application: Mapped[Application] = relationship("Application", back_populates="certificate")
    result: Mapped[Result | None] = relationship("Result")
    pdf_document: Mapped[Document | None] = relationship("Document", foreign_keys=[pdf_document_id])
    issued_by_user: Mapped[User | None] = relationship("User", foreign_keys=[issued_by_user_id])
    revoked_by_user: Mapped[User | None] = relationship("User", foreign_keys=[revoked_by_user_id])
