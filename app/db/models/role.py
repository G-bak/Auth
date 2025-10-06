"""Role SQLAlchemy model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Role(Base):
    """Persisted representation of a permission role."""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    level = Column(Integer, unique=True, nullable=False)

    users = relationship("User", secondary="user_roles", back_populates="roles")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"Role(id={self.id!r}, name={self.name!r}, level={self.level!r})"