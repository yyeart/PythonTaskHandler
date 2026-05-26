import asyncio

from src.core.execution_exceptions import QueueClosedError
from src.models.task import Task


class AsyncTaskQueue:
    def __init__(self, maxsize: int) -> None:
        self._queue: asyncio.Queue[Task] = asyncio.Queue(maxsize=maxsize)
        self._closed: bool = False

    async def put(self, task: Task) -> None:
        if self._closed:
            raise QueueClosedError('Queue is closed')
        await self._queue.put(task)

    async def get(self) -> Task:
        return await self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()

    async def join(self) -> None:
        await self._queue.join()

    def close(self) -> None:
        self._closed = True
