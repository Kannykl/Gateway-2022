"""Fixtures for database tests"""
import uuid

import motor.motor_asyncio
import pytest
from fastapi.encoders import jsonable_encoder

from database_api.config import DATABASE_CONTAINER_NAME
from database_api.config import DATABASE_PORT
from main import app


@pytest.fixture()
async def clear_test_users_db():
    """Clear database with users collection"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    yield
    await app.mongodb["users"].delete_many({})


@pytest.fixture()
async def clear_test_bots_db():
    """Clear database with bots collection"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    yield
    await app.mongodb["bots"].delete_many({})


@pytest.fixture()
async def clear_test_tasks_collections():
    """Clear database with bots collection"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    yield
    await app.mongodb["tasks"].delete_many({})


@pytest.fixture()
def valid_user_data():
    """Valid user data for registration"""
    return {
        "user": {
            "email": "user@example.com",
            "password": "12345678",
            "password2": "12345678",
        }
    }


@pytest.fixture()
def user_to_insert():
    """Valid data to create a user"""
    return {
        "_id": uuid.uuid4(),
        "email": "user@example.com",
        "hashed_password": "uasfahfklafa",
    }


@pytest.fixture()
async def test_db_with_one_test_user(user_to_insert):
    """Test db with one user"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    new_user = jsonable_encoder(user_to_insert)
    await app.mongodb["users"].insert_one(new_user)
    yield

    await app.mongodb["users"].delete_many({})


@pytest.fixture()
def create_bot_data():
    """Valid data to create a bot"""
    return {"bot": {"username": "test_bot", "password": "bot_password"}}


@pytest.fixture()
def bot_to_insert():
    """Valid bot data to insert in database"""
    return {
        "_id": "123-fdsfa",
        "username": "bot_to_insert",
        "password": "bot_to_insert_password",
        "is_busy": False,
    }


@pytest.fixture()
def busy_bot_to_insert():
    """Bot with busy status"""
    return {
        "_id": "gfdgl",
        "username": "bot_to_insert_2",
        "password": "bot_to_insert_password",
        "is_busy": True,
    }


@pytest.fixture()
async def test_db_with_one_bot(bot_to_insert):
    """Test db with one bot"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    new_bot = jsonable_encoder(bot_to_insert)
    await app.mongodb["bots"].insert_one(new_bot)
    yield

    await app.mongodb["bots"].delete_many({})


@pytest.fixture()
async def test_db_with_one_busy_bot(busy_bot_to_insert):
    """Test db with one busy bot"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    new_bot = jsonable_encoder(busy_bot_to_insert)
    await app.mongodb["bots"].insert_one(new_bot)
    yield

    await app.mongodb["bots"].delete_many({})


@pytest.fixture()
def new_password_for_user():
    """New password for user"""
    return "new_password_for_user"


@pytest.fixture()
def new_email_for_user():
    """New email for user"""
    return "new_email_for_user@example.com"


@pytest.fixture()
def create_bot_task_data():
    """Valid create bot tasks data"""
    return {
        "task": {"owner": "user@example.com", "status": "PENDING", "count": 1}
    }


@pytest.fixture()
async def test_task_collection_with_one_bot_task(task_to_insert):
    """Test db with one user"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    new_task = jsonable_encoder(task_to_insert)
    await app.mongodb["tasks"].insert_one(new_task)
    yield

    await app.mongodb["tasks"].delete_many({})


@pytest.fixture()
def task_to_insert():
    """Valid data to create a bot task"""
    return {
        "_id": str(uuid.uuid4()),
        "owner": "user@example.com",
        "status": "PENDING",
        "count": 1,
    }


@pytest.fixture()
def boost_task_to_insert():
    """Valid data to create a boost task"""
    return {
        "task": {
            "_id": str(uuid.uuid4()),
            "owner": "user@example.com",
            "status": "PENDING",
            "count": 1,
            "boost_type": "like",
            "link": "http://test_url.com",
        }
    }


@pytest.fixture()
def free_bot_to_insert():
    """Bot with busy status"""
    return {
        "_id": "free_bot_id",
        "username": "bot_to_insert_2",
        "password": "bot_to_insert_password",
        "is_busy": False,
        "is_deleted": False,
    }


@pytest.fixture()
async def test_db_with_one_free_bot(free_bot_to_insert):
    """Test db with one busy bot"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    new_bot = jsonable_encoder(free_bot_to_insert)
    await app.mongodb["bots"].insert_one(new_bot)
    yield

    await app.mongodb["bots"].delete_many({})


@pytest.fixture()
async def test_task_collection_with_one_boost_task(boost_task_to_insert):
    """Test db with one user"""
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}"
    )
    app.mongodb = app.mongodb_client["test_db"]

    new_task = jsonable_encoder(boost_task_to_insert)
    await app.mongodb["tasks"].insert_one(new_task)
    yield

    await app.mongodb["tasks"].delete_many({})
