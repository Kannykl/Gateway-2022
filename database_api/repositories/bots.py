from database_api.models.bot import Bot, BotIn
from database_api.repositories.base import BaseRepository
from database_api.repositories.mongo_helper import parse_objects


class BotRepository(BaseRepository):
    """Encapsulate work with bots instance."""

    COLLECTION_NAME: str = "bots"

    async def get(self, count: int = 100) -> list[Bot] | None:
        cursor = self.database[BotRepository.COLLECTION_NAME].find()
        documents = [document for document in await cursor.to_list(length=count)]

        return parse_objects(documents)

    async def create(self, u: BotIn) -> Bot:
        bot = Bot(
            username=u.username,
            password=u.password
        )

        await self.database[BotRepository.COLLECTION_NAME].insert_one(bot.dict())

        return bot

    async def delete(self, username: str):
        await self.database[BotRepository.COLLECTION_NAME].delete_many({"username": username})
