"""Role domain entity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RoleEntity:
    """Representation of a permission role."""

    id: int | None
    name: str
    level: int

    @classmethod
    def from_orm(cls, model) -> "RoleEntity":  # type: ignore[override]
        return cls(id=model.id, name=model.name, level=model.level)