from src.core.models import Task
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
        logger.info('Получены 3 задачи из API')
        return [
            Task(id=1, payload={'status': 'error', 'color': 'red'}),
            Task(id=2, payload={'status': 'waiting', 'color': 'yellow'}),
            Task(id=3, payload={'status': 'success', 'color': 'green'}),
        ]

    def __repr__(self) -> str:
        return 'API'
