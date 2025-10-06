"""Shared pytest fixtures."""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings


@pytest.fixture(scope="session", autouse=True)
def configure_settings(tmp_path_factory: pytest.TempPathFactory) -> Generator[None, None, None]:
    db_path = tmp_path_factory.mktemp("db") / "test.db"
    os.environ.update(
        {
            "SECRET_KEY": "test-secret-key",
            "DATABASE_URL": f"sqlite:///{db_path}",
            "SUPERUSER_EMAIL": "owner@example.com",
            "SUPERUSER_PASSWORD": "OwnerPass123",
        }
    )
    get_settings.cache_clear()  # type: ignore[attr-defined]
    yield
    get_settings.cache_clear()  # type: ignore[attr-defined]


@pytest.fixture()
def app_instance(configure_settings):
    from app.main import create_app

    return create_app()


@pytest.fixture()
def client(app_instance) -> Generator[TestClient, None, None]:
    with TestClient(app_instance) as client:
        yield client