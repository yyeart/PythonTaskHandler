from typing import Iterator

from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class ApiSource:
    """Класс, представляющий источник данных из API."""
    def get_tasks(self) -> Iterator[Task]:
        """
        Метод-заглушка для получения задач из API.

        :returns: Итераторы задач, полученных из API.
        :rtype: Iterator[Task]
        """
        logger.info('REST request...')
        data = [
            {'id': 1, 'description': 'Finish lab', 'priority': 'very urgent!!!'},
            {'id': 1, 'description': 'Finish lab', 'priority': 1, 'status': 'In_progress'},
            # {'id': 1, 'description': 'Duplicate ID example', 'priority': 2},
            {'id': 2, 'description': 'Chill', 'priority': 3},
            {'id': 3, 'description': 'Touch grass', 'priority': 10}
        ]
        logger.info(f'Claimed {len(data)} tasks from API')
        for payload in data:
            try:
                yield Task(**payload) # type: ignore[arg-type]
            except (TaskError, ValueError) as e:
                logger.warning(f'Failed to get task from API: {e}')

    def __repr__(self) -> str:
        return 'API'
