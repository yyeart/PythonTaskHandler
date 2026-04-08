from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger

class ApiSource:
    """Класс, представляющий источник данных из API."""
    def get_tasks(self) -> list[Task]:
        """
        Метод-заглушка для получения задач из API.

        :returns: Список задач, полученных из API.
        :rtype: list[Task]
        """
        print('REST запрос...')
        data = [
            {'id': 1, 'description': 'Finish lab', 'priority': 'very urgent!!!'},
            {'id': 1, 'description': 'Finish lab', 'priority': 1},
            {'id': 1, 'description': 'Duplicate ID example', 'priority': 2},
            {'id': 2, 'description': 'Chill', 'priority': 3}
        ]
        logger.info(f'Получено {len(data)} задач из API')
        tasks = []
        for payload in data:
            try:
                tasks.append(Task(**payload)) # type: ignore[arg-type]
            except (TaskError, ValueError) as e:
                logger.error(f'Failed to get task from API: {e}')
        return tasks

    def __repr__(self) -> str:
        return 'API'
