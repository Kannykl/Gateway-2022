from fastapi.encoders import jsonable_encoder

from database_api.models.bot import Bot, BotIn
from database_api.repositories.base import BaseRepository


class BotRepository(BaseRepository):
    """Encapsulate work with bots instance."""

    COLLECTION_NAME: str = "bots"

    async def get(self, count: int = 100) -> list[Bot] | None:
        cursor = self.database[BotRepository.COLLECTION_NAME].find()
        documents = [jsonable_encoder(document) for document in await cursor.to_list(length=count)]

        return documents

    async def create(self, u: BotIn) -> Bot:
        bot = Bot(
            username=u.username,
            password=u.password
        )

        new_bot = jsonable_encoder(bot)

        await self.database[BotRepository.COLLECTION_NAME].insert_one(new_bot)

        return Bot.parse_obj(new_bot)

    async def delete(self, username: str):
        await self.database[BotRepository.COLLECTION_NAME].delete_many({"username": username})

    async def get_by_username(self, username: str) -> Bot | None:
        bot = await self.database[BotRepository.COLLECTION_NAME].find_one({"username": username})

        if not bot:
            return None

        return Bot.parse_obj(bot)

    async def busy(self, username: str) -> Bot:
        await self.database[BotRepository.COLLECTION_NAME].\
            update_one({'username': username}, {'$set': {'is_busy': True}})

        updated_bot = await self.database[BotRepository.COLLECTION_NAME].find_one({'username': username})

        return Bot.parse_obj(updated_bot)

    async def free(self, username: str) -> Bot:
        await self.database[BotRepository.COLLECTION_NAME]. \
            update_one({'username': username}, {'$set': {'is_busy': False}})

        updated_bot = await self.database[BotRepository.COLLECTION_NAME].find_one({'username': username})

        return Bot.parse_obj(updated_bot)
