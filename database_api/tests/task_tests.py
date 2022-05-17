import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_create_bot_task(clear_test_tasks_collections, create_bot_task_data):
    """Test create bot task"""
    async with AsyncClient(app=app, base_url="http://localhost/db/") as async_client:
        response = await async_client.post("create_task/bot/", json=create_bot_task_data)

    new_bot = response.json()

    assert response.status_code == 200
    assert new_bot["owner"] == "user@example.com"
    assert new_bot["status"] == "PENDING"
    assert new_bot["count"] == 1


@pytest.mark.asyncio
async def test_update_task_status(test_task_collection_with_one_bot_task, task_to_insert):
    """Test update task status"""

    assert task_to_insert["status"] == "PENDING"

    async with AsyncClient(app=app, base_url="http://localhost/db/") as async_client:
        response = await async_client.patch("update_task/", params={
            "task_id": task_to_insert["_id"],
            "task_status": "SUCCESS",
        })

    task = response.json()

    assert response.status_code == 200
    assert task["status"] == "SUCCESS"
    assert task['_id'] == task_to_insert["_id"]


@pytest.mark.asyncio
async def test_create_boost_task(test_task_collection_with_one_boost_task, boost_task_to_insert):
    """Test create boost task"""

    assert boost_task_to_insert["task"]["status"] == "PENDING"

    async with AsyncClient(app=app, base_url="http://localhost/db/") as async_client:
        response = await async_client.post("create_task/boost/", json=boost_task_to_insert)

    boost_task = response.json()

    assert response.status_code == 200
    assert boost_task["_id"] == boost_task_to_insert["task"]["_id"]
    assert boost_task["status"] == "PENDING"
    assert boost_task["owner"] == "user@example.com"
