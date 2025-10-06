"""JSON Web Token helpers."""

from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()


def encode(payload: Dict[str, Any], expires_minutes: int | None = None) -> str:
    """Encode the provided payload into a signed JWT."""

    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode(token: str) -> Dict[str, Any]:
    """Decode a JWT token."""

    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:  # pragma: no cover
        raise ValueError("Invalid token") from exc