from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository for User model data access."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone."""
        return self.db.query(User).filter(User.phone == phone).first()

    def get_by_identifier(self, identifier: str) -> Optional[User]:
        """Get user by email or phone identifier."""
        return self.db.query(User).filter(
            (User.email == identifier) | (User.phone == identifier)
        ).first()

    def email_exists(self, email: str, exclude_user_id: Optional[str] = None) -> bool:
        """Check if email exists."""
        query = self.db.query(User).filter(User.email == email)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None

    def phone_exists(self, phone: str, exclude_user_id: Optional[str] = None) -> bool:
        """Check if phone exists."""
        query = self.db.query(User).filter(User.phone == phone)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None

    def create_user(
        self,
        full_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password_hash: str = None,
        role: str = None,
        is_active: bool = True,
        is_verified: bool = False,
    ) -> User:
        """Create a new user."""
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            role=role,
            is_active=is_active,
            is_verified=is_verified,
        )
        self.db.add(user)
        self.db.flush()  # Flush to get the generated ID but don't commit yet
        return user

    def update_last_login(self, user_id: str) -> Optional[User]:
        """Update last login timestamp for user."""
        from datetime import datetime

        user = self.get_by_id(user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            self.db.add(user)
        return user

    def save(self, user: User) -> User:
        """Save user changes."""
        self.db.add(user)
        self.db.flush()
        return user

    def commit(self):
        """Commit transaction."""
        self.db.commit()

    def rollback(self):
        """Rollback transaction."""
        self.db.rollback()
