import json
from pathlib import Path
from typing import Iterator

from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class FileSource:
    """Класс, представляющий источник данных из файла."""
    def __init__(self, path: str | Path):
        self.path = path
        self._tasks: list[Task] | None = None

    def _load_tasks(self) -> list[Task]:
        """
        Метод для получения задач из файла.

        :returns: Список объектов Task
        :rtype: list[Task]
        """
        tasks = []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f'File error: {e}')
            return []
        if isinstance(data, list):
            for item in data:
                try:
                    tasks.append(Task(**item))
                except (ValueError, TaskError, TypeError) as e:
                    logger.warning(f'Invalid task skipped: {e}')
        return tasks

    def get_tasks(self) -> Iterator[Task]:
        if self._tasks is None:
            self._tasks = self._load_tasks()
        return iter(self._tasks)

    def __repr__(self) -> str:
        return 'Файловый источник'
