from main import app
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_valid_user(clear_test_users_db, valid_user_data):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("/db/create_user/", json=valid_user_data)
    assert response.status_code == 201
    new_user = response.json()
    assert new_user['email'] == "user@example.com"
    assert new_user['is_admin'] is False


@pytest.mark.asyncio
async def test_get_users(test_db_with_one_test_user):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"/db/get_users/1")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_user_by_email(test_db_with_one_test_user):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"/db/get_user_by_email/?email=user@example.com")
    assert response.status_code == 200
    user = response.json()
    assert user['email'] == "user@example.com"
