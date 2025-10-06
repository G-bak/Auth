"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health probe")
def health_check() -> dict[str, str]:
    return {"status": "ok"}