"""Unit tests for domain entities."""

from datetime import datetime

from app.domain.entities import UserEntity
from app.domain.value_objects import Email


def test_user_entity_role_checks() -> None:
    entity = UserEntity(id=1, email=Email("user@example.com"), role_levels=[1, 3], created_at=datetime.utcnow())
    assert entity.has_level(1) is True
    assert entity.has_level(2) is False
    entity.attach_roles([2, 4])
    assert entity.role_levels == [2, 4]
    assert entity.has_level(3) is True