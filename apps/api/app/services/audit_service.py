from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit import AuditLog


class AuditService:
    """Service for audit logging."""

    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        """
        Create an audit log entry.
        
        Args:
            action: Type of action (USER_REGISTERED, USER_LOGIN_SUCCESS, etc.)
            user_id: ID of the user performing the action
            resource_type: Type of resource being acted upon
            resource_id: ID of the resource being acted upon
            details: Additional details about the action
            ip_address: IP address of the requester
        
        Returns:
            Created AuditLog object
        """
        audit_log = AuditLog(
            action=action,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            created_at=datetime.utcnow(),
        )
        self.db.add(audit_log)
        self.db.flush()
        return audit_log

    def commit(self):
        """Commit audit log changes."""
        try:
            self.db.commit()
        except Exception as e:
            # Don't let audit logging failure crash the request
            self.db.rollback()
            print(f"Warning: Audit log failed to commit: {e}")

    def log_user_registered(self, user_id: str, role: str, identifier: str):
        """Log user registration."""
        self.log_action(
            action="USER_REGISTERED",
            user_id=user_id,
            resource_type="User",
            resource_id=user_id,
            details={"role": role, "identifier": identifier},
        )
        self.commit()

    def log_login_success(self, user_id: str, ip_address: Optional[str] = None):
        """Log successful login."""
        self.log_action(
            action="USER_LOGIN_SUCCESS",
            user_id=user_id,
            resource_type="User",
            resource_id=user_id,
            ip_address=ip_address,
        )
        self.commit()

    def log_login_failed(self, identifier: str, ip_address: Optional[str] = None):
        """Log failed login attempt."""
        self.log_action(
            action="USER_LOGIN_FAILED",
            resource_type="User",
            details={"identifier": identifier},
            ip_address=ip_address,
        )
        self.commit()

    def log_password_changed(self, user_id: str):
        """Log password change."""
        self.log_action(
            action="PASSWORD_CHANGED",
            user_id=user_id,
            resource_type="User",
            resource_id=user_id,
        )
        self.commit()
