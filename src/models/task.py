from datetime import datetime

from src.core.exceptions import StateError, TaskError
from src.core.constants import ALLOWED_STATUSES, ALLOWED_STATUS_TRANSITIONS
from src.models.descriptors.numeric import IntRange
from src.models.descriptors.other import Const, CreatedAt, FullInfoDescriptor
from src.models.descriptors.text import NotEmptyString
from src.logger.setup_logger import logger


class Task:
    """
    Структура данных задачи
    """
    __slots__ = ('_id', '_description', '_priority', '_created_at', '_status', '__dict__')
    _ids: set[int] = set()

    id = Const()
    description = NotEmptyString()
    priority = IntRange(1, 10)
    created_at = CreatedAt()
    full_info = FullInfoDescriptor()

    def __init__(self, id: int, description: str, priority: int = 1, status: str | None = 'Planned'):
        if id in Task._ids:
            logger.error('Failed to create task. Id duplicate found')
            raise TaskError(f'task with ID {id} already exists.')
        self.id = id
        self.description = description
        self.priority = priority
        self._status = status if status is not None else 'Planned'
        self._created_at: datetime
        setattr(self, '_created_at', datetime.now())
        Task._ids.add(id)
        logger.info('Task was created')

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: str):
        logger.info('Attempt to set a new status')
        if new_status not in ALLOWED_STATUSES:
            logger.error('Attempt failed: forbidden status')
            raise ValueError(f'{new_status} is an unknown status.'
                             f'Allowed statuses: {ALLOWED_STATUSES}')
        if new_status not in ALLOWED_STATUS_TRANSITIONS[self._status]:
            logger.error('Attempt failed: forbidden transition')
            raise StateError(
                f'transition from {self._status} to {new_status} is not allowed'
            )
        logger.info(f'Task {self.id}: status changed from {self.status} to {new_status}')
        self._status = new_status

    @property
    def is_executable(self) -> bool:
        return self.status == 'Planned' and self.priority > 0 and len(self.description) > 0

    @classmethod
    def _clear_ids(cls):
        """
        Функция, очищающая set с id всех существующих задач.
        Используется только для тестирования!
        """
        cls._ids.clear()
