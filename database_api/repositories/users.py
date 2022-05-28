"""User repository"""
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from authentication_api.core.security import hash_password
from authentication_api.models.user import User
from authentication_api.models.user import UserIn
from database_api.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Encapsulates work with user instance in database."""

    COLLECTION_NAME: str = "users"

    async def get(self, count: int = 100) -> list[User] | None:
        """Get count users from db"""
        cursor = self.database[UserRepository.COLLECTION_NAME].find()
        documents = [
            jsonable_encoder(document)
            for document in await cursor.to_list(length=count)
        ]

        return documents

    async def get_by_email(self, email: EmailStr) -> User | None:
        """Get user by email from db"""
        user = await self.database[UserRepository.COLLECTION_NAME].find_one(
            {"email": email}
        )

        if not user:
            return None

        return User.parse_obj(user)

    async def create(self, user_in: UserIn) -> User:
        """Create one user in db"""
        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
        )
        new_user = jsonable_encoder(user)

        await self.database[UserRepository.COLLECTION_NAME].insert_one(
            new_user
        )

        return User.parse_obj(new_user)

    async def delete(self, email: EmailStr):
        """Delete one user from db"""
        await self.database[UserRepository.COLLECTION_NAME].delete_many(
            {"email": email}
        )

    async def update_password(self, email: EmailStr, new_password) -> User:
        """Update user password for user in db"""
        self.database[UserRepository.COLLECTION_NAME].update_one(
            {"email": email},
            {"$set": {"hashed_password": hash_password(new_password)}},
        )

        updated_user = await self.database[
            UserRepository.COLLECTION_NAME
        ].find_one({"email": email})

        return User.parse_obj(updated_user)

    async def update_email(self, email: EmailStr, new_email: EmailStr) -> User:
        """Update user email with one new"""
        self.database[UserRepository.COLLECTION_NAME].update_one(
            {"email": email}, {"$set": {"email": new_email}}
        )

        updated_user = await self.database[
            UserRepository.COLLECTION_NAME
        ].find_one({"email": new_email})

        return User.parse_obj(updated_user)
