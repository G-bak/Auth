"""API integration tests for authentication flows."""

from fastapi.testclient import TestClient


def test_register_and_login_flow(client: TestClient) -> None:
    register_payload = {
        "email": "tester@example.com",
        "password": "Password123!",
        "full_name": "테스터",
    }
    response = client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == register_payload["email"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["email"] == register_payload["email"]


def test_login_requires_valid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "absent@example.com", "password": "invalidpass"},
    )
    assert response.status_code == 401