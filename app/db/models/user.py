"""User SQLAlchemy model."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    """Persisted representation of an application user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    roles = relationship("Role", secondary="user_roles", back_populates="users")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"User(id={self.id!r}, email={self.email!r})"