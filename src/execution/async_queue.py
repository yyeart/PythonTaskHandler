import asyncio

from src.core.execution_exceptions import QueueClosedError
from src.models.task import Task



class AsyncTaskQueue:
    """Асинхронная очередь"""
    def __init__(self, maxsize: int) -> None:
        self._queue: asyncio.Queue[Task | object] = asyncio.Queue(maxsize=maxsize)
        self._closed: bool = False

    async def put(self, task: Task) -> None:
        """Поместить таску в очередь, если она не закрыта"""
        if self._closed:
            raise QueueClosedError('Queue is closed')
        await self._queue.put(task)

    async def get(self) -> Task | object:
        """
        Возвращает следующий элемент из очереди, если она не закрыта и не пуста

        :returns: Задача
        :rtype: Task | object
        """
        if not self._queue.empty():
            return self._queue.get_nowait()
        if self._closed:
            raise QueueClosedError('Queue is closed and empty')
        while self._queue.empty() and not self._closed:
            try:
                return await asyncio.wait_for(self._queue.get(), timeout=0.05)
            except asyncio.TimeoutError:
                continue
        if self._closed and self._queue.empty():
            raise QueueClosedError('Queue is closed and empty')
        return self._queue.get_nowait()

    def task_done(self) -> None:
        """Помечает текущий элемент как обработанный"""
        self._queue.task_done()

    async def join(self) -> None:
        """Блокирует до тех пор, пока не будут обработны все элементы"""
        await self._queue.join()

    def close(self) -> None:
        """Помечает очередь как закрытую, чтобы запретить дальнейшую отправку"""
        self._closed = True
