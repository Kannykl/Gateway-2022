"""Endpoints for database requests"""
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status
from pydantic import EmailStr

from authentication_api.models.user import User
from authentication_api.models.user import UserIn
from config import logger
from database_api.endpoints.depends import get_bot_repository
from database_api.endpoints.depends import get_task_repository
from database_api.endpoints.depends import get_user_repository
from database_api.models.bot import Bot
from database_api.models.bot import BotIn
from database_api.models.task import BoostTask
from database_api.models.task import Task
from database_api.repositories.bots import BotRepository
from database_api.repositories.tasks import TaskRepository
from database_api.repositories.users import UserRepository

db_router = APIRouter()


@db_router.get(
    "/get_users/",
    response_model=list[User],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    count: int, users: UserRepository = Depends(get_user_repository)
):
    """Get count users from database."""
    return await users.get(count)


@db_router.get(
    "/get_user_by_email/",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_email(
    email: EmailStr,
    users: UserRepository = Depends(get_user_repository),
):
    """Get user by email."""
    return await users.get_by_email(email)


@db_router.post(
    "/create_user/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserIn = Body(..., embed=True),
    users: UserRepository = Depends(get_user_repository),
):
    """Create user with email."""
    logger.info(f"User {user.email} created")

    return await users.create(user)


@db_router.delete("/delete_user/", status_code=status.HTTP_200_OK)
async def delete_user(
    email: EmailStr,
    users: UserRepository = Depends(get_user_repository),
):
    """Delete one user from database."""
    logger.info(f"User {email} deleted")

    return await users.delete(email)


@db_router.patch(
    "/update_user_password/",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def update_user_password(
    email: EmailStr,
    new_password: str,
    users: UserRepository = Depends(get_user_repository),
):
    """Update user password with one new."""
    logger.info(f"User {email} updated password")

    return await users.update_password(email, new_password)


@db_router.patch(
    "/update_user_email/",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def update_user_email(
    email: EmailStr,
    new_email: EmailStr,
    users: UserRepository = Depends(get_user_repository),
):
    """Update user password with one new."""
    logger.info(f"User {email} updated email to {new_email}")

    return await users.update_email(email, new_email)


@db_router.post(
    "/create_bot/",
    response_model=Bot,
    status_code=status.HTTP_201_CREATED,
)
async def create_bot(
    bot: BotIn = Body(..., embed=True),
    bots: BotRepository = Depends(get_bot_repository),
):
    """Create one new bot in database."""
    logger.info(f"Bot {bot.username} created")

    return await bots.create(bot)


@db_router.delete("/delete_bot/", status_code=status.HTTP_200_OK)
async def delete_bot(
    username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Delete one bot from database."""
    logger.info(f"Bot {username} deleted")

    return await bots.delete(username)


@db_router.patch(
    "/update_bot/free/",
    response_model=Bot,
    status_code=status.HTTP_200_OK,
)
async def set_free_bot_status(
    username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Free the bot from a job."""
    logger.info(f"Status changed to free for bot {username}")

    return await bots.free(username)


@db_router.patch(
    "/update_bot/busy/",
    response_model=Bot,
    status_code=status.HTTP_200_OK,
)
async def set_busy_bot_status(
    username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Switch bot status to busy."""
    logger.info(f"Status changed to busy for bot {username}")

    return await bots.busy(username)


@db_router.get(
    "/get_bot_by_username/",
    response_model=Bot,
    status_code=status.HTTP_200_OK,
)
async def get_bot_by_username(
    username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Get one bot from database"""
    return await bots.get_by_username(username)


@db_router.get(
    "/get_bots/",
    response_model=list[Bot],
    status_code=status.HTTP_200_OK,
)
async def get(
    count: int = 100,
    bots: BotRepository = Depends(get_bot_repository),
):
    """Get count bots from database"""
    return await bots.get(count)


@db_router.post(
    "/create_task/bot/",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
async def create_bot_task(
    task: Task = Body(..., embed=True),
    tasks: TaskRepository = Depends(get_task_repository),
):
    """Create one new task."""
    return await tasks.create_bot_task(task)


@db_router.patch(
    "/update_task/",
    response_model=Task,
    status_code=status.HTTP_200_OK,
)
async def update_task_status(
    task_id: str,
    task_status: str,
    tasks: TaskRepository = Depends(get_task_repository),
):
    """Update task status to success and add finish time."""
    return await tasks.update_status(task_id, task_status)


@db_router.get(
    "/get_free_bots/",
    response_model=list[Bot],
    status_code=status.HTTP_200_OK,
)
async def get_free_bots(
    count: int = 100,
    bots: BotRepository = Depends(get_bot_repository),
):
    """Get free bots from database."""
    return await bots.get_free_bots(count)


@db_router.post(
    "/create_task/boost/",
    response_model=BoostTask,
    status_code=status.HTTP_200_OK,
)
async def create_boost_task(
    task: BoostTask = Body(..., embed=True),
    tasks: TaskRepository = Depends(get_task_repository),
):
    """Create one new task."""
    return await tasks.create_boost_task(task)


@db_router.get(
    "/get_bot_for_work/",
    response_model=Bot,
    status_code=status.HTTP_200_OK,
)
async def get_bot(bots: BotRepository = Depends(get_bot_repository)):
    """Get free bot for work from database."""
    return await bots.get_bot_for_work()


@db_router.patch(
    "/update_bot/delete/", response_model=Bot, status_code=status.HTTP_200_OK
)
async def update_bot_delete(
    username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Set delete flag to True"""
    return await bots.set_deleted_status(username)


@db_router.patch(
    "/update_bot/recover/", response_model=Bot, status_code=status.HTTP_200_OK
)
async def update_bot_recover(
    username: str, bots: BotRepository = Depends(get_bot_repository)
):
    """Set delete flag to True"""
    return await bots.recover(username)


@db_router.get(
    "/get_valid_bots/",
    response_model=list[Bot],
    status_code=status.HTTP_200_OK,
)
async def get_valid_bots(
    count: int = 100, bots: BotRepository = Depends(get_bot_repository)
):
    """Get count bots from database"""
    return await bots.get_valid_bots(count)


@db_router.patch(
    "/free_and_recover_bots/",
    response_model=list[Bot],
    status_code=status.HTTP_200_OK,
)
async def free_and_recover_all_bots(
    bots: BotRepository = Depends(get_bot_repository),
):
    """Get count bots from database"""
    return await bots.free_and_recover_all_bots()
