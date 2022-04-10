import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from authentication_api.core.security import create_access_token, hash_password
from authentication_api.models.user import User
from database_api.repositories.users import UserRepository
from main import app

client = TestClient(app)


async def user_with_wrong_password():
    return User(
        email="user@mail.ru",
        hashed_password=hash_password("NotVeryGoodPass123")
    )


async def user_get_by_email():
    return User(
        email="user@mail.ru",
        hashed_password=hash_password("VeryGoodPass123")
    )


async def no_user_found():
    return None


async def test_create_user():
    return {
        "_id": "sdf312fds",
        "email": "user@mail.ru",
        "is_admin": False,
        "hashed_password": "fdsf142asfg-sfds"
    }


def mock_init_db(*args, **kwargs):
    pass


def mock_create_user(*args, **kwargs):
    return test_create_user()


def mock_no_user_found(*args, **kwargs):
    return no_user_found()


def mock_get_user(*args, **kwargs):
    return user_get_by_email()


def mock_get_user_with_wrong_password(*args, **kwargs):
    return user_with_wrong_password()


def test_valid_login(monkeypatch, login_user_data):
    monkeypatch.setattr(UserRepository, "get_by_email", mock_get_user)
    monkeypatch.setattr(UserRepository, "__init__", mock_init_db)

    json_data = jsonable_encoder(login_user_data)

    response = client.post("/auth/login", json=json_data)

    token = response.json()

    assert response.status_code == 200
    assert token["access_token"] == create_access_token({"sub": login_user_data.email})


def test_valid_register(monkeypatch, register_user_data):
    monkeypatch.setattr(UserRepository, "get_by_email", mock_no_user_found)
    monkeypatch.setattr(UserRepository, "create", mock_create_user)
    monkeypatch.setattr(UserRepository, "__init__", mock_init_db)

    response = client.post("/auth/register", json=register_user_data)

    new_user = response.json()

    assert response.status_code == 200

    assert new_user["email"] == register_user_data["email"]


def test_login_with_wrong_password(monkeypatch, login_user_data):
    monkeypatch.setattr(UserRepository, "get_by_email", mock_get_user_with_wrong_password)
    monkeypatch.setattr(UserRepository, "__init__", mock_init_db)

    json_data = jsonable_encoder(login_user_data)

    response = client.post("/auth/login", json=json_data)

    assert response.status_code == 401


def test_register_existing_user(monkeypatch, register_user_data):
    monkeypatch.setattr(UserRepository, "get_by_email", mock_get_user)
    monkeypatch.setattr(UserRepository, "__init__", mock_init_db)

    response = client.post("/auth/register", json=register_user_data)

    assert response.status_code == 409
