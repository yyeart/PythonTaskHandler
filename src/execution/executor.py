import asyncio

from src.core.async_contract import TaskHandler
from src.execution.async_queue import AsyncTaskQueue
from src.execution.resources import ExecutionSession
from src.execution.stats import ExecutionStats
from src.models.task import Task
from src.core.execution_exceptions import HandlerNotFoundError, ExecutionError, QueueClosedError, TaskExecutionError
from src.logger.setup_logger import logger


class TaskExecutor:
    """Исполнитель задач с помощью пула асинхронных воркеров и обработчиков"""
    def __init__(self, handlers: list[TaskHandler], worker_count: int = 2) -> None:
        for handler in handlers:
            if not isinstance(handler, TaskHandler):
                raise ExecutionError(f'{type(handler).__name__} is not TaskHandler instance')
        self._handlers: list[TaskHandler] = handlers
        if worker_count < 1:
            raise ExecutionError('Worker count must be >= 1')
        self._worker_count: int = worker_count
        self._workers: list[asyncio.Task] = []
        self.execution_queue = AsyncTaskQueue(maxsize=100)
        self.stats = ExecutionStats()
        self._started: bool = False

    def _resolve_handler(self, task: Task) -> TaskHandler:
        """
        Возвращает первого обработчика, способного обработать задачу

        :param task: Задача для обработки
        :type task: Task
        :returns: Обработчик
        :rtype: TaskHandler
        """
        for handler in self._handlers:
            if handler.can_handle(task):
                return handler
        raise HandlerNotFoundError(f'No handler found for task {task.id}')

    async def start(self) -> None:
        """Запуск пула воркеров"""
        if self._started:
            logger.warning('TaskExecutor is already running')
            return
        logger.info(f'Starting TaskExecutor with {self._worker_count} workers...')
        for i in range(self._worker_count):
            self._workers.append(asyncio.create_task(self._worker(i+1, self.execution_queue)))
        self._started = True

    async def submit_task(self, task: Task) -> None:
        """Отправляет задачу на асинхронную обработку"""
        if not self._started:
            raise RuntimeError('Executor is not started')
        await self.execution_queue.put(task)
        logger.info(f'Producer pushed task {task.id} in queue')

    async def _worker(self, worker_id: int, queue: AsyncTaskQueue) -> None:
        """
        Извлекает задачи из очереди и выполняет с помощью обработчиков

        :param worker_id: Идентификатор воркера
        :type worker_id: int
        :param queue: Очередь с задачами
        :type queue: AsyncTaskQueue
        """
        while True:
            try:
                task: Task = await queue.get() # type: ignore[assignment]
            except QueueClosedError:
                logger.info(f'Worker {worker_id} exited (Queue is closed)')
                break
            try:
                handler = self._resolve_handler(task)
                logger.info(f'Worker {worker_id} took task {task.id}')
            except HandlerNotFoundError as e:
                self.stats.add_skipped()
                logger.warning(f'Worker {worker_id} skipped task {task.id}: {e}')
                queue.task_done()
                continue
            try:
                session_id = f'w{worker_id}-t{task.id}'
                async with ExecutionSession(session_id=session_id, stats=self.stats):
                    await handler.handle(task)
            except TaskExecutionError as e:
                task.status = 'Failed'
                logger.error(f'Worker {worker_id} could not handle task {task.id}: {e}')
            except Exception as e:
                task.status = 'Failed'
                logger.critical(f'Worker {worker_id} crashed while executing task {task.id}: {e}')
            finally:
                queue.task_done()

    async def stop(self) -> None:
        """Останавливает исполнитель и дожидается завершения воркеров"""
        if not self._started:
            return
        logger.info('Stopping TaskExecutor...')
        self.execution_queue.close()
        logger.info('Waiting for workers to finish remaining tasks...')
        await asyncio.gather(*self._workers)
        self._started = False
        logger.info('TaskExecutor stopped')
        print(self.stats.get_summary())
