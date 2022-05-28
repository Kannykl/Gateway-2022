"""Task repository"""

from fastapi.encoders import jsonable_encoder

from database_api.models.task import Task, BoostTask
from database_api.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    """Encapsulates work with task instance in database."""

    COLLECTION_NAME: str = "tasks"

    async def create_bot_task(self, task: Task):
        new_task = jsonable_encoder(task)

        await self.database[TaskRepository.COLLECTION_NAME].insert_one(new_task)

        return Task.parse_obj(new_task)

    async def update_status(self, task_id: str, status: str):
        """Update task status"""
        self.database[TaskRepository.COLLECTION_NAME]. \
            update_one({'_id': task_id},
                       {'$set': {'status': status}})

        updated_user = await self.database[TaskRepository.COLLECTION_NAME]. \
            find_one({'_id': task_id})

        return Task.parse_obj(updated_user)

    async def create_boost_task(self, task: BoostTask):
        new_task = jsonable_encoder(task)

        await self.database[TaskRepository.COLLECTION_NAME].insert_one(new_task)

        return BoostTask.parse_obj(new_task)
