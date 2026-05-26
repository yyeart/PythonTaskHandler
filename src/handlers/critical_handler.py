import asyncio

from src.core.execution_exceptions import TaskExecutionError
from src.models.task import Task
from src.logger.setup_logger import logger


class CriticalTaskHandler:
    name = 'critical'

    def can_handle(self, task: Task) -> bool:
        return task.status == 'Planned' and task.priority > 8

    async def handle(self, task: Task) -> None:
        if not self.can_handle(task):
            logger.warning(f'[CRITICAL] Cannot handle task {task.id}')
            raise TaskExecutionError(f'Cannot handle task {task.id}')
        logger.info(f"[CRITICAL] Started handling task {task.id}")
        task.status = 'In_progress'
        await asyncio.sleep(0.01)
        task.status = 'Done'
        logger.info(f'[CRITICAL] Task {task.id} completed')
