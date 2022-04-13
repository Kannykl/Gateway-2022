"""Tests for authentication methods"""

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from httpx import Response
from authentication_api.core.security import create_access_token, hash_password
from main import app


client = TestClient(app)


async def user_with_wrong_password():
    """User data with password that doesnt matching with login password"""
    response = Response(
        status_code=200,
        json={
            "email": "user@mail.ru",
            "hashed_password": hash_password("NotVeryGoodPass123"),
        },
    )

    return response


async def user_get_by_email():
    """Returns response with user"""
    response = Response(
        status_code=200,
        json={
            "email": "user@mail.ru",
            "hashed_password": hash_password("VeryGoodPass123"),
        },
    )

    return response


async def no_user_found():
    """Returns response with no user"""
    response = Response(status_code=200, json={})
    return response


async def create_test_user():
    """Return response with data to create user"""
    response = Response(
        status_code=200,
        json={
            "_id": "sdf312fds",
            "email": "user@mail.ru",
            "is_admin": False,
            "hashed_password": "fdsf142asfg-sfds",
        },
    )
    return response


def mock_create_user(*args, **kwargs):
    """Mock create user"""
    return create_test_user()


def mock_no_user_found(*args, **kwargs):
    """Mock no user found"""
    return no_user_found()


def mock_get_user(*args, **kwargs):
    """Mock get user"""
    return user_get_by_email()


def mock_get_user_with_wrong_password(*args, **kwargs):
    """Mock get user with wrong password"""
    return user_with_wrong_password()


def test_valid_login(monkeypatch, login_user_data, async_client):
    """Test login user with valid credentials"""
    monkeypatch.setattr(app.async_client, "get", mock_get_user)

    json_data = jsonable_encoder(login_user_data)

    response = client.post("/auth/login", json=json_data)

    token = response.json()

    assert response.status_code == 200
    assert token["access_token"] == create_access_token({"sub": login_user_data.email})


def test_valid_register(monkeypatch, register_user_data, async_client):
    """Test register user with valid credentials"""
    monkeypatch.setattr(app.async_client, "get", mock_no_user_found)
    monkeypatch.setattr(app.async_client, "post", mock_create_user)

    response = client.post("/auth/register", json=register_user_data)

    new_user = response.json()

    assert response.status_code == 200

    assert new_user["email"] == register_user_data["email"]


def test_login_with_wrong_password(monkeypatch, login_user_data, async_client):
    """Test login user with invalid credentials"""
    monkeypatch.setattr(app.async_client, "get", mock_get_user_with_wrong_password)

    json_data = jsonable_encoder(login_user_data)

    response = client.post("/auth/login", json=json_data)

    assert response.status_code == 401


def test_register_existing_user(monkeypatch, register_user_data, async_client):
    """Test register existing user"""
    monkeypatch.setattr(app.async_client, "get", mock_get_user)

    response = client.post("/auth/register", json=register_user_data)

    assert response.status_code == 409
