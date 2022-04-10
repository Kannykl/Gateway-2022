from database_api.repositories.users import UserRepository
from database_api.repositories.bots import BotRepository
from fastapi import Request


def get_user_repository(request: Request) -> UserRepository:
    return UserRepository(request)


def get_bot_repository(request: Request) -> BotRepository:
    return BotRepository(request)