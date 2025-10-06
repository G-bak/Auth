"""SQLAlchemy models for AuthService."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .role import Role  # noqa: E402  pylint: disable=wrong-import-position
from .user import User  # noqa: E402  pylint: disable=wrong-import-position
from .user_role import UserRole  # noqa: E402  pylint: disable=wrong-import-position

__all__ = ["Base", "User", "Role", "UserRole"]