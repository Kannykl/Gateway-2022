import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_bot(clear_test_bots_db, create_bot_data):
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.post("create_bot/", json=create_bot_data)

    new_bot = response.json()

    assert response.status_code == 201
    assert new_bot["username"] == "test_bot"
    assert new_bot["password"] == "bot_password"
    assert new_bot["is_busy"] is False


@pytest.mark.asyncio
async def test_delete_bot(test_db_with_one_bot, bot_to_insert):
    assert await app.mongodb['bots'].count_documents({}) == 1

    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.delete(f"delete_bot/?username={bot_to_insert['username']}")

    assert response.status_code == 200
    assert await app.mongodb['bots'].count_documents({}) == 0


@pytest.mark.asyncio
async def test_set_free_bot_status(test_db_with_one_busy_bot, busy_bot_to_insert):
    assert busy_bot_to_insert['is_busy'] is True

    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.patch(f"update_bot/free/?username={busy_bot_to_insert['username']}")

    update_bot = response.json()

    assert response.status_code == 200
    assert update_bot['is_busy'] is False


@pytest.mark.asyncio
async def test_set_busy_bot_status(test_db_with_one_bot, bot_to_insert):
    assert bot_to_insert['is_busy'] is False

    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.patch(f"update_bot/busy/?username={bot_to_insert['username']}")

    update_bot = response.json()

    assert response.status_code == 200
    assert update_bot['is_busy'] is True


@pytest.mark.asyncio
async def test_get_bot_by_username(test_db_with_one_bot, bot_to_insert):
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.get(f"get_bot_by_username/?username={bot_to_insert['username']}")

    found_bot = response.json()

    assert response.status_code == 200
    assert found_bot["username"] == bot_to_insert["username"]


@pytest.mark.asyncio
async def test_get_bots(test_db_with_one_bot, bot_to_insert):
    async with AsyncClient(app=app, base_url="http://localhost/db/") as ac:
        response = await ac.get(f"get_bots/?count=1")

    bots = response.json()

    assert bots[0]['username'] == bot_to_insert['username']
    assert response.status_code == 200

