"""Email value object ensuring canonical formatting."""

from dataclasses import dataclass

from pydantic import EmailStr


@dataclass(frozen=True)
class Email:
    """Typed wrapper for validated email addresses."""

    value: str

    def __post_init__(self) -> None:
        EmailStr.validate(self.value)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.value