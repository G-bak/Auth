"""Role routes."""

from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.permission import get_user_service, require_role_level
from app.domain import UserEntity, UserService
from app.schemas import RoleRead

router = APIRouter()


@router.get("/", response_model=List[RoleRead], summary="List available roles")
def list_roles(
    _: UserEntity = Depends(require_role_level(2)),
    user_service: UserService = Depends(get_user_service),
) -> List[RoleRead]:
    return [RoleRead(id=role.id, name=role.name, level=role.level) for role in user_service.list_roles()]