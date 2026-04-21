from typing import Iterator

from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class ApiSource:
    """Класс, представляющий источник данных из API."""
    def __init__(self) -> None:
        self._tasks: list[Task] | None = None

    def _load_tasks(self) -> list[Task]:
        """
        Метод-заглушка для получения задач из API.

        :returns: Список задач, полученных из API.
        :rtype: list[Task]
        """
        tasks = []
        print('REST запрос...')
        data = [
            {'id': 1, 'description': 'Finish lab', 'priority': 'very urgent!!!'},
            {'id': 1, 'description': 'Finish lab', 'priority': 1, 'status': 'In_progress'},
            {'id': 1, 'description': 'Duplicate ID example', 'priority': 2},
            {'id': 2, 'description': 'Chill', 'priority': 3}
        ]
        logger.info(f'Claimed {len(data)} tasks from API')
        for payload in data:
            try:
                tasks.append(Task(**payload)) # type: ignore[arg-type]
            except (TaskError, ValueError) as e:
                logger.warning(f'Failed to get task from API: {e}')
        return tasks

    def get_tasks(self) -> Iterator[Task]:
        if self._tasks is None:
            self._tasks = self._load_tasks()
        return iter(self._tasks)

    def __repr__(self) -> str:
        return 'API'
