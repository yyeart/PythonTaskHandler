import asyncio

from src.handlers.helpers import change_status
from src.models.task import Task


class LowPriorityTaskHandler:
    """Обработчик для задач низкого приоритета"""
    name = 'low_priority'

    def can_handle(self, task: Task) -> bool:
        return task.is_executable and task.priority < 4

    @change_status
    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0.5)
