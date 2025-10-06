"""Pydantic schemas for auth flows."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type indicator")
    expires_at: datetime | None = Field(None, description="Optional expiry timestamp")


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None
    role_levels: list[int] = Field(default_factory=list)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None