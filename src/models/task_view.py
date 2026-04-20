from typing import Callable


class TaskView:
    """
    Класс для ленивых операций над коллекцией TaskQueue
    """
    def __init__(self, iter_fact: Callable):
        self._iter_fact = iter_fact

    def __iter__(self):
        return self._iter_fact()

    def filter_by_priority(self, min_priority: int):
        return TaskView(
            lambda: (task for task in self if task.priority >= min_priority)
        )

    def filter_by_status(self, status: str):
        return TaskView(
            lambda: (task for task in self if task.status == status)
        )

    def _limited_iter(self, n: int):
        for i, item in enumerate(self):
            if i < n:
                yield item
            else:
                break

    def limit(self, n: int):
        return TaskView(lambda: self._limited_iter(n))
