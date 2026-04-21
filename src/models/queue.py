from typing import Iterator

from src.core.contract import TaskSource
from src.models.task import Task
from src.models.task_view import TaskView
from src.logger.setup_logger import logger


class TaskQueue:
    """Очередь задач"""
    def __init__(self) -> None:
        self.__sources: list[TaskSource] = []

    def add_source(self, source: TaskSource) -> None:
        """
        Загружает задачи из источника в очередь

        :param source: Источник задач, реализующий контракт TaskSource
        :type source: TaskSource
        :returns: Ничего не возвращает
        :rtype: None
        """
        self.__sources.append(source)
        logger.info(f'Source {source} was loaded')

    def __iter__(self) -> Iterator[Task]:
        for src in self.__sources:
            try:
                for task in src.get_tasks():
                    yield task
            except Exception as e:
                logger.warning(f"Source {src} raised an exception: {e}")

    def all(self) -> TaskView:
        return TaskView(lambda: iter(self))
