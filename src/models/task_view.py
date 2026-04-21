from typing import Callable, Iterator

from src.models.task import Task


class TaskView:
    """
    Класс для ленивых операций над коллекцией TaskQueue
    """
    def __init__(self, iter_fact: Callable[[], Iterator[Task]]):
        self._iter_fact = iter_fact

    def __iter__(self):
        return self._iter_fact()

    def filter_by_priority(self, min_priority: int) -> "TaskView":
        """
        :returns: Возвращает ленивое представление задач с приоритетом равному min_priority
        :rtype: TaskView
        """
        return TaskView(
            lambda: (task for task in self if task.priority >= min_priority)
        )

    def filter_by_status(self, status: str) -> "TaskView":
        """
        :returns: Возвращает ленивое представление задач со статусом равному status
        :rtype: TaskView
        """
        return TaskView(
            lambda: (task for task in self if task.status == status)
        )

    def _limited_iter(self, n: int) -> Iterator[Task]:
        for i, item in enumerate(self):
            if i < n:
                yield item
            else:
                break

    def limit(self, n: int) -> "TaskView":
        """
        Возвращает первые n задач по заданному фильтру
        При n = -1 выводятся все задачи
        """
        if n < 0:
            return TaskView(lambda: iter(self))
        return TaskView(lambda: self._limited_iter(n))
