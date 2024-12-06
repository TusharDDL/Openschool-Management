from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.enums import UserRole

def test_login_success(client: TestClient, test_users: dict[str, User]):
    user = test_users[UserRole.SUPER_ADMIN]
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user.email,
            "password": "superadmin123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, test_users: dict[str, User]):
    user = test_users[UserRole.SUPER_ADMIN]
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_register_user(
    client: TestClient,
    superadmin_token: str,
    test_tenant: dict
):
    response = client.post(
        "/api/v1/auth/register",
        headers={"Authorization": f"Bearer {superadmin_token}"},
        json={
            "email": "newuser@test.com",
            "username": "newuser",
            "password": "newuser123",
            "role": "teacher",
            "tenant_id": test_tenant.id
        }
    )
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_register_unauthorized(client: TestClient, student_token: str):
    response = client.post(
        "/api/v1/auth/register",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "email": "unauthorized@test.com",
            "username": "unauthorized",
            "password": "test123",
            "role": "teacher",
            "tenant_id": 1
        }
    )
    assert response.status_code == 403