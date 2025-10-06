"""Authentication domain logic."""

from datetime import datetime

from app.core.security import create_access_token, decode_access_token, verify_password
from app.domain.entities import UserEntity
from app.domain.services.user_service import UserService


class AuthService:
    """Coordinates authentication flows between HTTP and persistence layers."""

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def register(self, *, email: str, password: str, full_name: str | None = None) -> UserEntity:
        return self.user_service.create_user(email=email, password=password, full_name=full_name)

    def authenticate(self, *, email: str, password: str) -> tuple[UserEntity, str]:
        user = self.user_service.get_user_by_email(email)
        if not user or not verify_password(password, self._get_hashed_password(email)):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("Inactive account")
        token = create_access_token(subject=str(user.id), role_levels=user.role_levels)
        return user, token

    def _get_hashed_password(self, email: str) -> str:
        model = self.user_service.user_repo.get_by_email(email)
        if not model:
            raise ValueError("User not found")
        return model.hashed_password

    def verify_token(self, token: str) -> UserEntity:
        try:
            payload = decode_access_token(token)
        except ValueError as exc:  # pragma: no cover - delegated to tests
            raise ValueError("Token validation failed") from exc
        subject = payload.get("sub")
        if subject is None:
            raise ValueError("Token missing subject")
        user = self.user_service.get_user(int(subject))
        if not user:
            raise ValueError("User not found")
        return user

    def token_expired(self, token: str) -> bool:
        try:
            payload = decode_access_token(token)
        except ValueError:
            return True
        exp = payload.get("exp")
        if exp is None:
            return True
        return datetime.utcfromtimestamp(exp) <= datetime.utcnow()