from functools import wraps

from src.core.execution_exceptions import TaskExecutionError
from src.logger.setup_logger import logger
from src.models.task import Task


def change_status(func):
    @wraps(func)
    async def wrapper(self, task: Task, *args, **kwargs):
        if not self.can_handle(task):
            logger.warning(f'[{self.name.upper()}] Cannot handle task {task.id}')
            raise TaskExecutionError(f'Cannot handle task {task.id}')
        logger.info(f"[{self.name.upper()}] Started handling task {task.id}")
        task.status = 'In_progress'
        result = await func(self, task, *args, **kwargs)
        task.status = 'Done'
        logger.info(f'[{self.name.upper()}] Task {task.id} completed')
        return result
    return wrapper
