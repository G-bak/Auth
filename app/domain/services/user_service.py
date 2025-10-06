"""Domain service for user operations."""

from typing import Iterable, List, Optional

from app.domain.entities import RoleEntity, UserEntity
from app.domain.value_objects import Email
from app.utils.password import hash_password
from app.db.models import Role
from app.db.repositories import RoleRepository, UserRepository


class UserService:
    """High-level user orchestration that mediates between repositories and entities."""

    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo

    def list_users(self) -> List[UserEntity]:
        return [UserEntity.from_orm(user) for user in self.user_repo.list()]

    def get_user(self, user_id: int) -> Optional[UserEntity]:
        user = self.user_repo.get(user_id)
        return UserEntity.from_orm(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        user = self.user_repo.get_by_email(email)
        return UserEntity.from_orm(user) if user else None

    def create_user(self, *, email: str, password: str, full_name: str | None = None, default_level: int = 1) -> UserEntity:
        Email(email)  # validation
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already registered")
        hashed = hash_password(password)
        role = self.role_repo.get_by_level(default_level)
        roles: Iterable[Role] | None = [role] if role else None
        user = self.user_repo.create(email=email, hashed_password=hashed, full_name=full_name, roles=roles)
        return UserEntity.from_orm(user)

    def assign_role(self, user_id: int, level: int) -> UserEntity:
        user_model = self.user_repo.get(user_id)
        if not user_model:
            raise ValueError("User not found")
        role = self.role_repo.get_by_level(level)
        if not role:
            raise ValueError("Role not found")
        updated = self.user_repo.add_role(user_model, role)
        return UserEntity.from_orm(updated)

    def list_roles(self) -> List[RoleEntity]:
        return [RoleEntity.from_orm(role) for role in self.role_repo.list()]