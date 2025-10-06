"""Permission orchestration for RBAC."""

from app.domain.entities import UserEntity


class PermissionService:
    """Evaluate RBAC rules against user context."""

    def ensure_level(self, user: UserEntity, required_level: int) -> None:
        if not user.has_level(required_level):
            raise PermissionError("Insufficient role level")