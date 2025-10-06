"""API package exposing versioned routes."""

from fastapi import APIRouter

from .routes import v1_router

api_router = APIRouter()
api_router.include_router(v1_router)

__all__ = ["api_router"]