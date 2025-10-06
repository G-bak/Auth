"""User management routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.permission import get_user_service, require_role_level
from app.domain import UserEntity, UserService
from app.schemas import UserRead

router = APIRouter()


def _to_schema(user: UserEntity) -> UserRead:
    return UserRead(
        id=user.id or 0,
        email=str(user.email),
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        role_levels=user.role_levels,
    )


@router.get("/", response_model=List[UserRead], summary="List all users")
def list_users(
    _: UserEntity = Depends(require_role_level(4)),
    user_service: UserService = Depends(get_user_service),
) -> List[UserRead]:
    return [_to_schema(user) for user in user_service.list_users()]


@router.get("/{user_id}", response_model=UserRead, summary="Retrieve a user by id")
def get_user(
    user_id: int,
    _: UserEntity = Depends(require_role_level(3)),
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _to_schema(user)