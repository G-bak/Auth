"""User schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int
    created_at: datetime | None = None
    role_levels: list[int] = Field(default_factory=list)

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None