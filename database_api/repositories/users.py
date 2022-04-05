from pydantic import EmailStr
from authentication_api.core.security import hash_password
from authentication_api.models.user import User, UserIn
from database_api.repositories.base import BaseRepository
from database_api.repositories.mongo_helper import parse_objects


class UserRepository(BaseRepository):
    """Encapsulates work with user instance in database."""

    COLLECTION_NAME: str = "users"

    async def get(self, count: int = 100) -> list[User] | None:
        cursor = self.database[UserRepository.COLLECTION_NAME].find()
        documents = [document for document in await cursor.to_list(length=count)]

        return parse_objects(documents)

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

        await self.database[UserRepository.COLLECTION_NAME].insert_one(user.dict())

        return user