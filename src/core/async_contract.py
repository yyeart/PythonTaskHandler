from typing import Protocol, runtime_checkable

from src.models.task import Task


@runtime_checkable
class TaskHandler(Protocol):
    """Контракт обработчика"""
    name: str

    def can_handle(self, task: Task) -> bool:
        """
        Метод проверяющий условия работы определенного обработчика

        :param task: Задача для проверки
        :type task: Task
        :returns: True/False в зависимости от того, может ли обработчик справиться с задачей
        :rtype: bool
        """
        ...

    async def handle(self, task: Task) -> None:
        """
        Метод обработки задачи

        :param task: Задача
        :type task: Task
        """
        ...
