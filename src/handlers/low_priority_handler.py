import asyncio

from src.core.execution_exceptions import TaskExecutionError
from src.models.task import Task
from src.logger.setup_logger import logger


class LowPriorityTaskHandler:
    name = 'low_priority'

    def can_handle(self, task: Task) -> bool:
        return task.status == 'Planned' and task.priority < 4

    async def handle(self, task: Task) -> None:
        if not self.can_handle(task):
            logger.warning(f'[LOW] Cannot handle task {task.id}')
            raise TaskExecutionError(f'Cannot handle task {task.id}')
        logger.info(f"[LOW] Started handling task {task.id}")
        task.status = 'In_progress'
        await asyncio.sleep(0.5)
        task.status = 'Done'
        logger.info(f'[LOW] Task {task.id} completed')
