"""Reusable FastAPI dependencies for permission checks."""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.db.repositories import RoleRepository, UserRepository
from app.db.session import get_session
from app.domain import AuthService, PermissionService, UserEntity, UserService

OAuth2Token = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login"))]


def get_user_service(session=Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    role_repo = RoleRepository(session)
    return UserService(repo, role_repo)


def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)


def get_permission_service() -> PermissionService:
    return PermissionService()


def get_current_user(
    token: OAuth2Token,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserEntity:
    try:
        return auth_service.verify_token(token)
    except ValueError as exc:  # pragma: no cover - tested via API
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def require_role_level(level: int) -> Callable[[UserEntity], UserEntity]:
    def dependency(
        user: UserEntity = Depends(get_current_user),
        permission_service: PermissionService = Depends(get_permission_service),
    ) -> UserEntity:
        try:
            permission_service.ensure_level(user, level)
        except PermissionError as exc:  # pragma: no cover - tested via API
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
        return user

    return dependency