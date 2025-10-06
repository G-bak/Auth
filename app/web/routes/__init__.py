"""SSR route registration."""

from fastapi import APIRouter

from .auth import router as auth_router

web_router = APIRouter()
web_router.include_router(auth_router, prefix="/auth", tags=["web-auth"])

__all__ = ["web_router"]