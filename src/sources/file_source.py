import json
from pathlib import Path
from typing import Iterator

from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class FileSource:
    """Класс, представляющий источник данных из файла."""
    def __init__(self, path: str | Path) -> None:
        self.path = path

    def get_tasks(self) -> Iterator[Task]:
        """
        Метод для получения задач из файла.

        :returns: Итераторы объектов Task
        :rtype: Iterator[Task]
        """
        logger.info('File reading...')
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    try:
                        yield Task(**item)
                    except (ValueError, TaskError, TypeError) as e:
                        logger.warning(f'Invalid task skipped: {e}')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f'File error: {e}')

    def __repr__(self) -> str:
        return 'Файловый источник'
