import pytest

from authentication_api.models.token import Login


@pytest.fixture()
def login_user_data():
    return Login(
        email="user@mail.ru",
        password="VeryGoodPass123",
    )


@pytest.fixture()
def register_user_data():
    return {
        "email": "user@mail.ru",
        "password": "VeryGoodPass123",
        "password2": "VeryGoodPass123"
    }

