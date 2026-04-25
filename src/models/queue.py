from collections.abc import Callable, Iterator

from src.core.contract import TaskSource
from src.models.task import Task
from src.logger.setup_logger import logger


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
        return self._iterate_sources()

    def _iterate_sources(self) -> Iterator[Task]:
        for src in self.__sources:
            try:
                for task in src.get_tasks():
                    yield task
            except Exception as e:
                logger.warning(f"Source {src} raised an exception: {e}")

    def filter_by_priority(self, min_priority: int) -> "TaskQueue":
        """Возвращает ленивое представление задач с приоритетом выше или равному min_priority"""
        return TaskQueue(
            iter_factory=lambda: (task for task in self if task.priority <= min_priority)
        )

    def filter_by_status(self, status: str) -> "TaskQueue":
        """Возвращает ленивое представление задач с заданным статусом."""
        return TaskQueue(
            iter_factory=lambda: (task for task in self if task.status == status)
        )

    def _limited_iter(self, n: int) -> Iterator[Task]:
        for i, item in enumerate(self):
            if i < n:
                yield item
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
