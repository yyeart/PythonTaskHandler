import asyncio

from src.handlers.helpers import change_status
from src.models.task import Task


class StandardTaskHandler:
    name = 'standard'

    def can_handle(self, task: Task) -> bool:
        return task.is_executable and 4 <= task.priority <= 8

    @change_status
    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0.1)
