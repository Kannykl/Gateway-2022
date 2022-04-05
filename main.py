import motor.motor_asyncio
from fastapi import FastAPI
import uvicorn
from authentication_api.endpoints.auth import auth_router
from database_api.config import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from database_api.endpoints.database import db_router

app = FastAPI(title="Stat inc")

app.include_router(auth_router, prefix='/auth', tags=["auth"])
app.include_router(db_router, prefix='/db', tags=["database"])


@app.on_event("startup")
async def start_up_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_HOST, DATABASE_PORT)
    app.mongodb = app.mongodb_client[DATABASE_NAME]


@app.on_event("shutdown")
async def shutdown_mongodb_client():
    app.mongodb_client.close()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
