"""Endpoints for database requests"""

from fastapi import APIRouter, Depends, Body, status
from pydantic import EmailStr
from authentication_api.models.user import UserIn, User
from database_api.endpoints.depends import get_user_repository, get_bot_repository, get_task_repository
from database_api.models.bot import Bot, BotIn
from database_api.models.task import Task, BoostTask
from database_api.repositories.bots import BotRepository
from database_api.repositories.tasks import TaskRepository
from database_api.repositories.users import UserRepository

db_router = APIRouter()


@db_router.get("/get_users/", response_model=list[User], status_code=status.HTTP_200_OK)
async def get_users(count: int, users: UserRepository = Depends(get_user_repository)):
    """Get count users from database."""
    return await users.get(count)


@db_router.get(
    "/get_user_by_email/", response_model=User, status_code=status.HTTP_200_OK
)
async def get_user_by_email(
        email: EmailStr, users: UserRepository = Depends(get_user_repository)
):
    """Get user by email."""
    return await users.get_by_email(email)


@db_router.post(
    "/create_user/", response_model=User, status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: UserIn = Body(..., embed=True),
        users: UserRepository = Depends(get_user_repository),
):
    """Create user with email."""
    return await users.create(user)


@db_router.delete("/delete_user/", status_code=status.HTTP_200_OK)
async def delete_user(
        email: EmailStr, users: UserRepository = Depends(get_user_repository)
):
    """Delete one user from database."""
    return await users.delete(email)


@db_router.patch(
    "/update_user_password/", response_model=User, status_code=status.HTTP_200_OK
)
async def update_user_password(
        email: EmailStr,
        new_password: str,
        users: UserRepository = Depends(get_user_repository),
):
    """Update user password with one new."""
    return await users.update_password(email, new_password)


@db_router.patch(
    "/update_user_email/", response_model=User, status_code=status.HTTP_200_OK
)
async def update_user_email(
        email: EmailStr,
        new_email: EmailStr,
        users: UserRepository = Depends(get_user_repository),
):
    """Update user password with one new."""
    return await users.update_email(email, new_email)


@db_router.post("/create_bot/", response_model=Bot, status_code=status.HTTP_201_CREATED)
async def create_bot(
        bot: BotIn = Body(..., embed=True),
        bots: BotRepository = Depends(get_bot_repository),
):
    """Create one new bot in database."""
    return await bots.create(bot)


@db_router.delete("/delete_bot/", status_code=status.HTTP_200_OK)
async def delete_bot(username: str, bots: BotRepository = Depends(get_bot_repository)):
    """Delete one bot from database."""
    return await bots.delete(username)


@db_router.patch(
    "/update_bot/free/", response_model=Bot, status_code=status.HTTP_200_OK
)
async def set_free_bot_status(
        username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Free the bot from a job."""
    return await bots.free(username)


@db_router.patch(
    "/update_bot/busy/", response_model=Bot, status_code=status.HTTP_200_OK
)
async def set_busy_bot_status(
        username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Switch bot status to busy."""
    return await bots.busy(username)


@db_router.get(
    "/get_bot_by_username/", response_model=Bot, status_code=status.HTTP_200_OK
)
async def get_bot_by_username(
        username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Get one bot from database"""
    return await bots.get_by_username(username)


@db_router.get("/get_bots/", response_model=list[Bot], status_code=status.HTTP_200_OK)
async def get(count: int = 100, bots: BotRepository = Depends(get_bot_repository)):
    """Get count bots from database"""
    return await bots.get(count)


@db_router.post("/create_task/bot/", response_model=Task, status_code=status.HTTP_200_OK)
async def create_bot_task(task: Task = Body(..., embed=True),
                          tasks: TaskRepository = Depends(get_task_repository)
                          ):
    """Create one new task."""
    return await tasks.create_bot_task(task)


@db_router.patch("/update_task/", response_model=Task, status_code=status.HTTP_200_OK)
async def update_task_status(task_id: str, task_status: str, tasks: TaskRepository = Depends(get_task_repository)):
    """Update task status."""
    return await tasks.update_status(task_id, task_status)


@db_router.get("/get_free_bots/", response_model=list[Bot], status_code=status.HTTP_200_OK)
async def get_free_bots(count: int = 100, bots: BotRepository = Depends(get_bot_repository)):
    """Get free bots from database."""
    return await bots.get_free_bots(count)


@db_router.post("/create_task/boost/", response_model=BoostTask, status_code=status.HTTP_200_OK)
async def create_boost_task(task: BoostTask = Body(..., embed=True),
                            tasks: TaskRepository = Depends(get_task_repository)
                            ):
    """Create one new task."""
    return await tasks.create_boost_task(task)
