from main import app
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_valid_user(clear_test_users_db, valid_user_data):
<<<<<<< HEAD
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.post("create_user/", json=valid_user_data)
=======
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("/db/create_user/", json=valid_user_data)
>>>>>>> origin/db_tests
    assert response.status_code == 201
    new_user = response.json()
    assert new_user['email'] == "user@example.com"
    assert new_user['is_admin'] is False


@pytest.mark.asyncio
async def test_get_users(test_db_with_one_test_user):
<<<<<<< HEAD
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.get(f"get_users/?count=1")
=======
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"/db/get_users/1")
>>>>>>> origin/db_tests
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
<<<<<<< HEAD
async def test_get_user_by_email(test_db_with_one_test_user, user_to_insert):
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.get(f"get_user_by_email/?email={user_to_insert['email']}")
    assert response.status_code == 200
    user = response.json()
    assert user['email'] == "user@example.com"


@pytest.mark.asyncio
async def test_delete_user(test_db_with_one_test_user, user_to_insert):
    assert await app.mongodb['users'].count_documents({}) == 1

    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.delete(f"delete_user/?email={user_to_insert['email']}")

    assert response.status_code == 200
    assert await app.mongodb['users'].count_documents({}) == 0


@pytest.mark.asyncio
async def test_update_user_password(test_db_with_one_test_user, user_to_insert, new_password_for_user):
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.patch(f"update_user_password/?email={user_to_insert['email']}"
                                  f"&new_password={new_password_for_user}")

    assert response.status_code == 200


async def test_update_user_email(test_db_with_one_test_user, user_to_insert, new_email_for_user):
    assert user_to_insert["email"] == "user@example.com"

    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.patch(f"update_user_email/?email={user_to_insert['email']}"
                                  f"&new_email={new_email_for_user}")

    updated_user = response.json()
    assert response.status_code == 200
    assert updated_user['email'] == new_email_for_user
=======
async def test_get_user_by_email(test_db_with_one_test_user):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(f"/db/get_user_by_email/?email=user@example.com")
    assert response.status_code == 200
    user = response.json()
    assert user['email'] == "user@example.com"
>>>>>>> origin/db_tests
