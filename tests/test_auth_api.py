from fastapi.testclient import TestClient


def test_register_and_login_flow(client: TestClient):
    register_payload = {
        "email": "admin@example.com",
        "full_name": "Admin",
        "password": "password123",
        "role_level": 5,
    }

    response = client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == register_payload["email"]
    assert data["role_level"] == register_payload["role_level"]

    login_response = client.post(
        "/api/auth/login",
        data={"username": register_payload["email"], "password": register_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200, login_response.text
    token_data = login_response.json()
    assert "access_token" in token_data

    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == register_payload["email"]

    list_response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    )
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1