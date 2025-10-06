"""Permission-related schemas."""

from pydantic import BaseModel


class RoleRead(BaseModel):
    id: int | None = None
    name: str
    level: int

    class Config:
        orm_mode = True