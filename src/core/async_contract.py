from typing import Protocol, runtime_checkable

from src.models.task import Task


@runtime_checkable
class TaskHandler(Protocol):
    """Контракт обработчика"""
    name: str

    def can_handle(self, task: Task) -> bool:
        ...

    async def handle(self, task: Task) -> None:
        ...
