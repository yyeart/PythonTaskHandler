import json
from pathlib import Path

from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class FileSource:
    """Класс, представляющий источник данных из файла."""
    def __init__(self, path: str | Path):
        self.path = path

    def get_tasks(self) -> list[Task]:
        """
        Метод для получения задач из файла.

        :returns: Список задач, полученных из файла.
        :rtype: list[Task]
        """
        print(f'Чтение из {self.path}...')
        tasks = []
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError('Данные из Json должны быть типа list')
            for item in data:
                try:
                    tasks.append(Task(id=item['id'],
                                      description=item['description'],
                                      priority=item['priority']))
                except (TaskError, ValueError) as e:
                    logger.error(f'Failed to get task from file: {e}')
            logger.info(f'Загружно {len(tasks)} задач из {self.path}')
        except FileNotFoundError:
            logger.error(f'{self.path}: файл не найден')
        except ValueError as e:
            logger.error(f'Ошибка парсинга {self.path}: {e}')
        except Exception as e:
            logger.error(f'Непредвиденная ошибка: {e}')

        return tasks

    def __repr__(self) -> str:
        return 'Файловый источник'
