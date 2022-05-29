"""Bot repository"""
from fastapi.encoders import jsonable_encoder

from database_api.models.bot import Bot
from database_api.models.bot import BotIn
from database_api.repositories.base import BaseRepository


class BotRepository(BaseRepository):
    """Encapsulate work with bots instance."""

    COLLECTION_NAME: str = "bots"

    async def get(self, count: int = 100) -> list[dict] | None:
        """Get count bots from db"""
        cursor = self.database[BotRepository.COLLECTION_NAME].find()
        documents = [
            jsonable_encoder(document)
            for document in await cursor.to_list(length=count)
        ]

        return documents

    async def create(self, bot_in: BotIn) -> Bot:
        """Create bot with BotIn parameters"""
        bot = Bot(username=bot_in.username, password=bot_in.password)

        new_bot = jsonable_encoder(bot)

        await self.database[BotRepository.COLLECTION_NAME].insert_one(new_bot)

        return Bot.parse_obj(new_bot)

    async def delete(self, username: str):
        """Delete one bot from db"""
        await self.database[BotRepository.COLLECTION_NAME].delete_many(
            {"username": username}
        )

    async def get_by_username(self, username: str) -> Bot | None:
        """Get one bot from db"""
        bot = await self.database[BotRepository.COLLECTION_NAME].find_one(
            {"username": username}
        )

        if not bot:
            return None

        return Bot.parse_obj(bot)

    async def busy(self, username: str) -> Bot:
        """Set status busy for a bot"""
        await self.database[BotRepository.COLLECTION_NAME].update_one(
            {"username": username}, {"$set": {"is_busy": True}}
        )

        updated_bot = await self.database[
            BotRepository.COLLECTION_NAME
        ].find_one({"username": username})

        return Bot.parse_obj(updated_bot)

    async def free(self, username: str) -> Bot | None:
        """Set status free for a bot"""
        await self.database[BotRepository.COLLECTION_NAME].update_one(
            {"username": username}, {"$set": {"is_busy": False}}
        )

        updated_bot = await self.database[
            BotRepository.COLLECTION_NAME
        ].find_one({"username": username})

        return Bot.parse_obj(updated_bot) if updated_bot else None

    async def get_free_bots(self, count: int = 100) -> list[Bot] | None:
        """Get bots with status=free."""

        cursor = self.database[BotRepository.COLLECTION_NAME].find(
            {"$and": [{"is_busy": False}, {"is_deleted": False}]}
        )
        documents = [
            jsonable_encoder(document)
            for document in await cursor.to_list(length=count)
        ]

        return documents

    async def get_bot_for_work(self):
        """Get free bot and set busy=true"""
        updated_bot = await self.database[
            BotRepository.COLLECTION_NAME
        ].find_one_and_update(
            {"$and": [{"is_deleted": False}, {"is_busy": False}]},
            {"$set": {"is_busy": True}},
        )

        return Bot.parse_obj(updated_bot) if updated_bot else None

    async def set_deleted_status(self, username: str) -> Bot | None:
        """Set is_deleted flag to True"""
        await self.database[BotRepository.COLLECTION_NAME].update_one(
            {"username": username}, {"$set": {"is_deleted": True}}
        )

        updated_bot = await self.database[
            BotRepository.COLLECTION_NAME
        ].find_one({"username": username})

        return Bot.parse_obj(updated_bot) if updated_bot else None

    async def recover(self, username: str) -> Bot | None:
        """Set deleted flag to False"""
        await self.database[BotRepository.COLLECTION_NAME].update_one(
            {"username": username}, {"$set": {"is_deleted": False}}
        )

        updated_bot = await self.database[
            BotRepository.COLLECTION_NAME
        ].find_one({"username": username})

        return Bot.parse_obj(updated_bot) if updated_bot else None

    async def get_valid_bots(self, count: int = 100) -> list[Bot] | None:
        """Get valid bots fom db"""
        cursor = self.database[BotRepository.COLLECTION_NAME].find(
            {"is_deleted": False}
        )
        documents = [
            jsonable_encoder(document)
            for document in await cursor.to_list(length=count)
        ]

        return documents

    async def free_and_recover_all_bots(self) -> list[Bot] | None:
        all_bots = await self.get()

        if all_bots:
            for bot in all_bots:
                await self.recover(bot["username"])
                await self.free(bot["username"])

        free_and_recover_bots = await self.get()

        return free_and_recover_bots
