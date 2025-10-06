"""Smoke tests for SSR routes."""

from fastapi.testclient import TestClient


def test_login_page_renders(client: TestClient) -> None:
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "로그인" in response.text


def test_register_page_renders(client: TestClient) -> None:
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert "회원가입" in response.text