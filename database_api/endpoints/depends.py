from database_api.repositories.users import UserRepository
from database_api.core.connection import db


def get_user_repository() -> UserRepository:
    return UserRepository(db)



