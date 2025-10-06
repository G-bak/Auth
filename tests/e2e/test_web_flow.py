"""End-to-end style tests for SSR flows."""

from fastapi.testclient import TestClient


def test_register_and_login_via_forms(client: TestClient) -> None:
    register_response = client.post(
        "/auth/register",
        data={"email": "formuser@example.com", "password": "Password123!", "full_name": "폼 유저"},
        follow_redirects=False,
    )
    assert register_response.status_code == 303

    login_response = client.post(
        "/auth/login",
        data={"email": "formuser@example.com", "password": "Password123!"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303
    assert login_response.headers["location"] == "/dashboard"

    dashboard_response = client.get("/dashboard")
    assert "환영합니다" in dashboard_response.text