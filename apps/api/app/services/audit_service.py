from typing import Optional, Any, Dict
from sqlalchemy.orm import Session

try:
    from app.models.audit import AuditLog
except ImportError:
    from app.models.audit_log import AuditLog

class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(self, action: str, entity_type: str, actor_user_id: Optional[str] = None, 
                   entity_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            actor_user_id=actor_user_id,
            entity_id=entity_id,
            metadata=metadata
        )
        self.db.add(log)
        self.db.commit()
        return log

    def log_user_registered(self, user_id: str, role: str, identifier: str):
        return self.log_action(
            action="USER_REGISTERED",
            entity_type="USER",
            actor_user_id=user_id,
            entity_id=user_id,
            metadata={"role": role, "identifier": identifier}
        )