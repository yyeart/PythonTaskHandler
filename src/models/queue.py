from typing import Iterator

from src.core.contract import TaskSource
from src.models.task import Task
from src.models.task_view import TaskView
from src.logger.setup_logger import logger


class TaskQueue:
    """Очередь задач"""
    def __init__(self) -> None:
        self.__tasks: list[Task] = []

    def add_source(self, source: TaskSource) -> None:
        """
        Загружает задачи из источника в очередь

        :param source: Источник задач, реализующий контракт TaskSource
        :type source: TaskSource
        :returns: Ничего не возвращает
        :rtype: None
        """
        init_count = len(self.__tasks)
        try:
            for task in source.get_tasks():
                self.__tasks.append(task)
            logger.info(f'Loaded {len(self.__tasks)-init_count} tasks from {source}')
        except Exception as e:
            logger.error(f'{source} raised an exception: {e}')

    def __iter__(self) -> Iterator[Task]:
        return iter(self.__tasks)

    def __len__(self) -> int:
        return len(self.__tasks)

    def __getitem__(self, index: int) -> Task:
        return self.__tasks[index]

    def all(self) -> TaskView:
        return TaskView(lambda: iter(self.__tasks))
