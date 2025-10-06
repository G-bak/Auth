"""Application configuration settings."""

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Configuration values for the AuthService application."""

    app_name: str = Field("Auth Service", description="Human readable service name")
    environment: str = Field("local", description="Deployment environment name")
    secret_key: str = Field(..., description="JWT signing secret")
    access_token_expire_minutes: int = Field(30, ge=1, description="Default JWT expiry in minutes")
    algorithm: str = Field("HS256", description="JWT signing algorithm")
    database_url: str = Field(
        "mysql+pymysql://user:password@localhost:3306/auth",
        description="Database connection URL",
    )
    allowed_hosts: List[str] = Field(default_factory=lambda: ["*"])
    superuser_email: str = Field("admin@example.com", description="Initial administrator email")
    superuser_password: str = Field("ChangeMe123!", description="Initial administrator password")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("database_url")
    def validate_database_url(cls, value: str) -> str:  # noqa: D401
        """Ensure SQLite URLs include a relative path prefix."""

        if value.startswith("sqlite") and ":" not in value.split("///", maxsplit=1)[-1]:
            raise ValueError("SQLite URL must include a file path, e.g. sqlite:///./auth.db")
        return value


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings instance."""

    return Settings()