"""Domain entities exposed for use across layers."""

from .role_entity import RoleEntity
from .user_entity import UserEntity

__all__ = ["UserEntity", "RoleEntity"]