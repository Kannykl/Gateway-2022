"""Dependencies of database endpoints"""
from fastapi import Request

from database_api.repositories.bots import BotRepository
from database_api.repositories.users import UserRepository


def get_user_repository(request: Request) -> UserRepository:
    """Get instance of user repository."""
    return UserRepository(request)


def get_bot_repository(request: Request) -> BotRepository:
    """Get instance of bot repository."""
    return BotRepository(request)


def get_task_repository(request: Request) -> TaskRepository:
    """Get instance of task repository."""
    return TaskRepository(request)
