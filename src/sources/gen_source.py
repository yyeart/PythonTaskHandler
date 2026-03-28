import random

from src.models.task import Task
from src.logger.setup_logger import logger
from src.core.constants import ALLOWED_STATUSES

class GeneratorSource:
    """Класс, представляющий источник данных, который генерирует задачи."""
    def __init__(self, task_cnt: int):
        self.task_cnt = task_cnt

    def get_tasks(self) -> list[Task]:
        """
        Метод для генерации задач.

        :returns: Список задач, сгенерированных источником.
        :rtype: list[Task]
        """
        print("Генерация задач...")
        try:
            tasks = [
                Task(id=random.randint(100, 1000),
                    description=f'Generated description {i}',
                    priority=random.randint(1, 10),
                    status=random.choice(ALLOWED_STATUSES)) for i in range(self.task_cnt)
            ]
            logger.info(f'Сгенерировано {self.task_cnt} задач')
            return tasks
        except Exception as e:
            logger.error(f'Ошибка генерации задач: {e}')
            return []

    def __repr__(self) -> str:
        return 'Генератор'
