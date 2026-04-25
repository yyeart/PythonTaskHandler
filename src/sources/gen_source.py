import random
from typing import Iterator

from src.models.task import Task
from src.logger.setup_logger import logger
from src.core.constants import ALLOWED_STATUSES

class GeneratorSource:
    """Класс, представляющий источник данных, который генерирует задачи."""
    def __init__(self, task_cnt: int) -> None:
        self.task_cnt = task_cnt

    def get_tasks(self) -> Iterator[Task]:
        """
        Метод для генерации задач.

        :returns: Итераторы задач, сгенерированных источником.
        :rtype: Iterator[Task]
        """
        print('Генерация задач...')
        for i in range(self.task_cnt):
            try:
                yield Task(
                    id=random.randint(100, 1000),
                    description=f'Generated description {i}',
                    priority=random.randint(1, 10),
                    status=random.choice(ALLOWED_STATUSES)
                )

            except Exception as e:
                logger.error(f'Generation error: {e}')

    def __repr__(self) -> str:
        return 'Генератор'
