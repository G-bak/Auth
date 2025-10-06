"""Security helpers wrapping password hashing and JWT utilities."""

from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt

from app.core.config import get_settings
from app.utils.password import hash_password, verify_password

settings = get_settings()


def create_access_token(subject: str, expires_minutes: int | None = None, **claims: Any) -> str:
    """Generate a signed JWT access token."""

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    payload: Dict[str, Any] = {"sub": subject, "exp": expire, **claims}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""

    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:  # pragma: no cover - delegated to tests
        raise ValueError("Invalid token") from exc

__all__ = [
    "create_access_token",
    "decode_access_token",
    "hash_password",
    "verify_password",
]