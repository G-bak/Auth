"""Versioned API routers."""

from fastapi import APIRouter

from .v1.auth import router as auth_router
from .v1.health import router as health_router
from .v1.roles import router as roles_router
from .v1.users import router as users_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health_router)
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(roles_router, prefix="/roles", tags=["roles"])

__all__ = ["v1_router"]