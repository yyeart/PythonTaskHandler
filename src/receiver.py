from typing import Any

from src.models.task import Task
from src.core.contract import TaskSource
from src.logger.setup_logger import logger

class TaskReceiver:
    """Класс, представляющий приемник задач, который может принимать задачи от различных источников."""
    def __init__(self):
        self._tasks: list[Task] = []

    def receive_tasks(self, sources: list[Any]) -> None:
        """
        Метод для получения задач от различных источников.

        :param sources: Список источников задач.
        :type sources: list[Any]
        :returns: Ничего не возвращает, задачи сохраняются внутри класса.
        """
        for src in sources:
            if isinstance(src, TaskSource):
                try:
                    init_count = len(self._tasks)
                    new_tasks = src.get_tasks()
                    self._tasks.extend(new_tasks)
                    count = len(self._tasks) - init_count
                    logger.info(f'Принято {count} задач от <{src}>')
                except Exception as e:
                    logger.error(f'{src} вызвал исключение: {e}')
            else:
                logger.warning(f'Ошибка: {src} не соответствует контракту')

    def get_received_tasks(self) -> list[Task]:
        """
        Метод для получения всех принятых задач.

        :returns: Список принятых задач.
        :rtype: list[Task]
        """
        return self._tasks
