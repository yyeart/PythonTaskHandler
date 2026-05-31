from collections.abc import Callable, Iterator

from src.core.contract import TaskSource
from src.models.task import Task
from src.logger.setup_logger import logger
from src.models.task_iterator import TaskIterator


class TaskQueue:
    """Повторно итерируемая коллекция задач с ленивыми операциями."""
    def __init__(self, iter_factory: Callable[[], Iterator[Task]] | None = None) -> None:
        self.__sources: list[TaskSource] = []
        self._iter_factory = iter_factory

    def add_source(self, source: TaskSource) -> None:
        """
        Добавляет источник задач в очередь

        :param source: Источник задач, реализующий контракт TaskSource
        :type source: TaskSource
        :returns: Ничего не возвращает
        :rtype: None
        """
        self.__sources.append(source)
        logger.info(f'Source {source} was loaded')

    def __iter__(self) -> Iterator[Task]:
        if self._iter_factory is not None:
            return self._iter_factory()
        return TaskIterator(self.__sources)

    def filter_by_priority(self, max_priority: int) -> "TaskQueue":
        """
        Возвращает ленивое представление задач с приоритетом выше max_priority
        (1 - самое важное, 10 - самое не важное)
        """
        if max_priority < 0:
            return TaskQueue(iter_factory=lambda: iter(self))
        return TaskQueue(
            iter_factory=lambda: (task for task in self if task.priority <= max_priority)
        )

    def filter_by_status(self, status: str) -> "TaskQueue":
        """Возвращает ленивое представление задач с заданным статусом."""
        return TaskQueue(
            iter_factory=lambda: (task for task in self if task.status == status)
        )

    def _limited_iter(self, n: int) -> Iterator[Task]:
        cnt = 0
        for task in self:
            if cnt < n:
                yield task
                cnt += 1
            else:
                break

    def limit(self, n: int) -> "TaskQueue":
        """
        Возвращает первые n задач по заданному фильтру
        При n = -1 выводятся все задачи
        """
        if n < 0:
            return TaskQueue(iter_factory=lambda: iter(self))
        return TaskQueue(iter_factory=lambda: self._limited_iter(n))
