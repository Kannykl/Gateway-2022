from fastapi import APIRouter, Depends, Body, status
from pydantic import EmailStr
from authentication_api.models.user import UserIn, User
from database_api.endpoints.depends import get_user_repository
from database_api.repositories.users import UserRepository

db_router = APIRouter()


@db_router.get("/get_users/{count}",
               response_model=list[User],
               response_model_exclude={"hashed_password"},
               status_code=status.HTTP_200_OK)
async def get_users(count: int, users: UserRepository = Depends(get_user_repository)):
    """Get {count} users from database."""
    return await users.get(count)


@db_router.get("/get_user_by_email/",
               response_model=User,
               response_model_exclude={"hashed_password"},
               status_code=status.HTTP_200_OK)
async def get_user_by_email(email: EmailStr, users: UserRepository = Depends(get_user_repository)):
    return await users.get_by_email(email)


@db_router.post("/create_user/",
                response_model=User,
                response_model_exclude={"hashed_password"},
                status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn = Body(..., embed=True), users: UserRepository = Depends(get_user_repository)):
    return await users.create(user)
