import asyncio

from src.core.execution_exceptions import TaskExecutionError
from src.models.task import Task
from src.logger.setup_logger import logger


class StandardTaskHandler:
    name = 'standard'

    def can_handle(self, task: Task) -> bool:
        return task.status == 'Planned' and 4 <= task.priority <= 8

    async def handle(self, task: Task) -> None:
        if not self.can_handle(task):
            logger.warning(f'[STANDARD] Cannot handle task {task.id}')
            raise TaskExecutionError(f'Cannot handle task {task.id}')
        logger.info(f"[STANDARD] Started handling task {task.id}")
        task.status = 'In_progress'
        await asyncio.sleep(0.1)
        task.status = 'Done'
        logger.info(f'[STANDARD] Task {task.id} completed')
