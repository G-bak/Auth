"""Role API tests."""

from fastapi.testclient import TestClient


def test_list_roles_requires_permission(client: TestClient) -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "OwnerPass123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.get("/api/v1/roles/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 5
    assert payload[-1]["level"] == 5


def test_roles_for_low_permission_user(client: TestClient) -> None:
    register_payload = {
        "email": "viewer@example.com",
        "password": "Password123!",
        "full_name": "뷰어",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    token = login_response.json()["access_token"]

    response = client.get("/api/v1/roles/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403