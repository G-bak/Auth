"""Data access helpers for roles."""

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.db.models import Role


class RoleRepository:
    """CRUD logic for role records."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_level(self, level: int) -> Optional[Role]:
        return self.session.query(Role).filter(Role.level == level).first()

    def get_by_name(self, name: str) -> Optional[Role]:
        return self.session.query(Role).filter(Role.name == name).first()

    def list(self) -> Iterable[Role]:
        return self.session.query(Role).order_by(Role.level.asc()).all()

    def ensure_roles(self, roles: dict[int, str]) -> None:
        """Ensure all roles exist; create any missing ones."""

        for level, name in roles.items():
            if not self.get_by_level(level):
                role = Role(level=level, name=name)
                self.session.add(role)
        self.session.commit()