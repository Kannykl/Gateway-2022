"""Fixtures for authentication tests"""

import pytest
from httpx import AsyncClient

from authentication_api.models.token import Login
from main import app


@pytest.fixture()
def login_user_data():
    """User data for logging in the system"""
    return Login(
        email="user@mail.ru",
        password="VeryGoodPass123",
    )


@pytest.fixture()
def register_user_data():
    """User data for registration in the system"""
    return {
        "email": "user@mail.ru",
        "password": "VeryGoodPass123",
        "password2": "VeryGoodPass123",
        "is_admin": False
    }


@pytest.fixture()
async def async_client():
    """Async client to make async requests"""
    app.async_client = AsyncClient(app=app, base_url="http://localhost")
