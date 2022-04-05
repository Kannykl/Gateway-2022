from pydantic import EmailStr
from authentication_api.core.security import hash_password
from authentication_api.models.user import User, UserIn
from database_api.repositories.base import BaseRepository
from fastapi.encoders import jsonable_encoder


class UserRepository(BaseRepository):
    """Encapsulates work with user instance in database."""

    COLLECTION_NAME: str = "users"

    async def get(self, count: int = 100) -> list[User] | None:
        cursor = self.database[UserRepository.COLLECTION_NAME].find()
        documents = [jsonable_encoder(document) for document in await cursor.to_list(length=count)]

        return documents

    async def get_by_email(self, email: EmailStr) -> User | None:
        user = await self.database[UserRepository.COLLECTION_NAME].find_one({'email': email})

        if not user:
            return None

        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        user = User(
            email=u.email,
            hashed_password=hash_password(u.password)
        )
        new_user = jsonable_encoder(user)

        await self.database[UserRepository.COLLECTION_NAME].insert_one(new_user)

        return User.parse_obj(new_user)
