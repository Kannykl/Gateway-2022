from database_api.repositories.users import UserRepository
from fastapi import Request


def get_user_repository(request: Request) -> UserRepository:
    return UserRepository(request)



