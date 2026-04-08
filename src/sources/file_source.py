import json
from pathlib import Path
from typing import Generator

from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class FileSource:
    """Класс, представляющий источник данных из файла."""
    def __init__(self, path: str | Path):
        self.path = path

    def get_tasks(self) -> Generator[Task, None, None]:
        """
        Метод для получения задач из файла.

        :returns: Генератор объектов Task
        :rtype: Generator[Task, None, None]
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f'File error: {e}')
            return
        if isinstance(data, list):
            for item in data:
                try:
                    yield Task(**item)
                except (ValueError, TaskError, TypeError) as e:
                    logger.warning(f'Invalid task skipped: {e}')

    def __repr__(self) -> str:
        return 'Файловый источник'
