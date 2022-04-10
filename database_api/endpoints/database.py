from fastapi import APIRouter, Depends, Body, status
from pydantic import EmailStr
from authentication_api.models.user import UserIn, User
from database_api.endpoints.depends import get_user_repository, get_bot_repository
from database_api.models.bot import Bot, BotIn
from database_api.repositories.bots import BotRepository
from database_api.repositories.users import UserRepository

db_router = APIRouter()


@db_router.get("/get_users/",
               response_model=list[User],
               response_model_exclude={"hashed_password"},
               status_code=status.HTTP_200_OK)
async def get_users(count: int, users: UserRepository = Depends(get_user_repository)):
    """Get count users from database."""
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


@db_router.delete("/delete_user/",
                  status_code=status.HTTP_200_OK)
async def delete_user(email: EmailStr, users: UserRepository = Depends(get_user_repository)):
    return await users.delete(email)


@db_router.patch("/update_user_password/",
                 response_model=User,
                 response_model_exclude={"hashed_password"},
                 status_code=status.HTTP_200_OK)
async def update_user_password(email: EmailStr,
                               new_password: str,
                               users: UserRepository = Depends(get_user_repository)):
    return await users.update_password(email, new_password)


@db_router.patch("/update_user_email/",
                 response_model=User,
                 response_model_exclude={"hashed_password"},
                 status_code=status.HTTP_200_OK)
async def update_user_email(email: EmailStr,
                            new_email: EmailStr,
                            users: UserRepository = Depends(get_user_repository)):
    return await users.update_email(email, new_email)


@db_router.post("/create_bot/",
                response_model=Bot,
                status_code=status.HTTP_201_CREATED)
async def create_bot(bot: BotIn = Body(..., embed=True), bots: BotRepository = Depends(get_bot_repository)):
    return await bots.create(bot)


@db_router.delete("/delete_bot/",
                  status_code=status.HTTP_200_OK)
async def delete_bot(username: str, bots: BotRepository = Depends(get_bot_repository)):
    return await bots.delete(username)


@db_router.patch("/update_bot/free/",
                 response_model=Bot,
                 status_code=status.HTTP_200_OK)
async def set_free_bot_status(username: str, bots: BotRepository = Depends(get_bot_repository)):
    return await bots.free(username)


@db_router.patch("/update_bot/busy/",
                 response_model=Bot,
                 status_code=status.HTTP_200_OK)
async def set_busy_bot_status(username: str, bots: BotRepository = Depends(get_bot_repository)):
    return await bots.busy(username)


@db_router.get("/get_bot_by_username/",
               response_model=Bot,
               status_code=status.HTTP_200_OK)
async def get_bot_by_username(username: str, bots: BotRepository = Depends(get_bot_repository)):
    return await bots.get_by_username(username)


@db_router.get("/get_bots/",
               response_model=list[Bot],
               status_code=status.HTTP_200_OK)
async def get(count: int, bots: BotRepository = Depends(get_bot_repository)):
    return await bots.get(count)
