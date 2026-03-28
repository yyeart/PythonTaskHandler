from typing import Protocol, runtime_checkable

from src.models.task import Task

@runtime_checkable
class TaskSource(Protocol):
    """Контракт источника задач"""
    def get_tasks(self) -> list[Task]:
        """Метод для получения задач"""
        ...
