import asyncio
from typing import List

from src.core.async_contract import TaskHandler
from src.execution.async_queue import AsyncTaskQueue
from src.execution.resources import ExecutionSession
from src.models.task import Task
from src.core.execution_exceptions import HandlerNotFoundError
from src.logger.setup_logger import logger


class TaskExecutor:
    def __init__(self, handlers: List[TaskHandler], worker_count: int = 2) -> None:
        self._handlers = handlers
        self._worker_count = worker_count
        self.execution_queue = AsyncTaskQueue(maxsize=100)

    def _resolve_handler(self, task: Task) -> TaskHandler:
        for handler in self._handlers:
            if handler.can_handle(task):
                return handler
        raise HandlerNotFoundError(f'No handler found for task {task.id}')

    async def submit_tasks(self, queue: AsyncTaskQueue, tasks: List[Task]) -> None:
        for task in tasks:
            await queue.put(task)
        logger.info('All tasks have been submitted to queue')

    async def _worker(self, worker_id: int, queue: AsyncTaskQueue) -> None:
        while True:
            task = await queue.get()
            try:
                handler = self._resolve_handler(task)
                logger.info(f'Worker {worker_id} took task {task.id}')
                async with ExecutionSession(session_id=1): # TODO: session_id logic (?)
                    await handler.handle(task)
            except Exception as e:
                logger.error(f'Worker {worker_id} failed on task {task.id}: {e}')
            finally:
                queue.task_done()

    async def run(self, tasks: List[Task]) -> None:
        producer_task = asyncio.create_task(self.submit_tasks(self.execution_queue, tasks))

        workers = []
        for i in range(self._worker_count):
            workers.append(asyncio.create_task(self._worker(i + 1, self.execution_queue)))

        await producer_task
        await self.execution_queue.join()

        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)
        logger.info('TaskExecutor finished processing all tasks')
