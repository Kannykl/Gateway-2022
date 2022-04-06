import uuid

import motor.motor_asyncio
import pytest
from fastapi.encoders import jsonable_encoder

from database_api.config import DATABASE_HOST, DATABASE_PORT
from main import app


@pytest.fixture()
async def clear_test_users_db():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_HOST, DATABASE_PORT)
    app.mongodb = app.mongodb_client["test_db"]

    yield
    await app.mongodb['users'].delete_many({})


@pytest.fixture()
def valid_user_data():
    return {
        "user": {
            "email": "user@example.com",
            "password": "12345678",
            "password2": "12345678"
        }
    }


@pytest.fixture()
def user_to_insert():
    return {
        "_id": uuid.uuid4(),
        "email": "user@example.com",
        "hashed_password": "uasfahfklafa",
    }


@pytest.fixture()
async def test_db_with_one_test_user(user_to_insert):
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_HOST, DATABASE_PORT)
    app.mongodb = app.mongodb_client["test_db"]

    new_user = jsonable_encoder(user_to_insert)
    app.mongodb['users'].insert_one(new_user)
    yield

    await app.mongodb['users'].delete_many({})


