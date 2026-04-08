from typing import Iterable, Protocol, runtime_checkable

from src.models.task import Task

@runtime_checkable
class TaskSource(Protocol):
    """Контракт источника задач"""
    def get_tasks(self) -> Iterable[Task]:
        """Метод для получения задач"""
        ...
