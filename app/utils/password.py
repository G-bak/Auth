"""Password hashing utilities."""

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash for the provided password."""

    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that the plain password matches the stored hash."""

    return _pwd_context.verify(plain_password, hashed_password)