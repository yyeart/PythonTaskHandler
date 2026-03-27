from typing import Protocol, runtime_checkable

from src.core.models import Task

@runtime_checkable
class TaskSource(Protocol):
    """Контракт источника задач"""
    def get_tasks(self) -> list[Task]:
        """Метод для получения задач"""
        ...
