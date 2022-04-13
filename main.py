import motor.motor_asyncio
from fastapi import FastAPI
import uvicorn
from httpx import AsyncClient
from fastapi.middleware.cors import CORSMiddleware

from authentication_api.endpoints.auth import auth_router
from database_api.config import DATABASE_CONTAINER_NAME, DATABASE_NAME, DATABASE_PORT
from database_api.endpoints.database import db_router

app = FastAPI(title="Stat inc")

app.include_router(auth_router, prefix='/auth', tags=["auth"])
app.include_router(db_router, prefix='/db', tags=["database"])


origins = [
    "http://localhost:8002",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_up_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{DATABASE_CONTAINER_NAME}:{DATABASE_PORT}')
    app.mongodb = app.mongodb_client[DATABASE_NAME]
    app.async_client = AsyncClient(app=app, base_url="http://localhost")


@app.on_event("shutdown")
async def shutdown_mongodb_client():
    app.mongodb_client.close()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
