import motor.motor_asyncio
from database_api.config import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_HOST, DATABASE_PORT)

db = client[DATABASE_NAME]
