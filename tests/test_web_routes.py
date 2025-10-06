from fastapi.testclient import TestClient


def test_register_form_submission(client: TestClient):
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert "Create Account" in response.text

    submit_response = client.post(
        "/auth/register",
        data={
            "email": "user@example.com",
            "full_name": "Web User",
            "password": "password123",
            "role_level": 2,
        },
        allow_redirects=False,
    )
    assert submit_response.status_code == 303
    assert submit_response.headers["location"] == "/auth/login"


def test_login_sets_cookie(client: TestClient):
    client.post(
        "/api/auth/register",
        json={
            "email": "cookie@example.com",
            "full_name": "Cookie",
            "password": "password123",
            "role_level": 3,
        },
    )
    login_response = client.post(
        "/auth/login",
        data={"email": "cookie@example.com", "password": "password123"},
        allow_redirects=False,
    )
    assert login_response.status_code == 303
    assert "access_token" in login_response.cookies