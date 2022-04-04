from fastapi import FastAPI
import uvicorn
from authentication_api.endpoints.auth import auth_router
from database_api.endpoints.database import db_router

app = FastAPI(title="Stat inc")
app.include_router(auth_router, prefix='/auth', tags=["auth"])
app.include_router(db_router, prefix='/db', tags=["database"])


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
