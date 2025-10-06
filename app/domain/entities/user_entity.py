"""User domain entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List

from app.domain.value_objects import Email


@dataclass
class UserEntity:
    """Rich domain representation of a user."""

    id: int | None
    email: Email
    full_name: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    role_levels: List[int] = field(default_factory=list)

    def has_level(self, level: int) -> bool:
        """Return True if the user possesses the provided permission level."""

        return any(assigned_level >= level for assigned_level in self.role_levels)

    @classmethod
    def from_orm(cls, model) -> "UserEntity":  # type: ignore[override]
        roles = getattr(model, "roles", [])
        return cls(
            id=model.id,
            email=Email(model.email),
            full_name=model.full_name,
            is_active=model.is_active,
            created_at=model.created_at,
            role_levels=[role.level for role in roles],
        )

    def attach_roles(self, levels: Iterable[int]) -> None:
        """Replace the current role levels with the provided collection."""

        self.role_levels = sorted(set(levels))