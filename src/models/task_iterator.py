from collections.abc import Iterator

from src.core.contract import TaskSource
from src.models.task import Task
from src.logger.setup_logger import logger


class TaskIterator:
    def __init__(self, sources: list[TaskSource]) -> None:
        self._sources_iter = iter(sources)
        self._curr_task_iter: Iterator[Task] | None = None
        self._curr_source: TaskSource | None = None
        self._ids: set[int] = set()

    def __iter__(self) -> "TaskIterator":
        return self

    def __next__(self) -> Task:
        while True:
            if self._curr_task_iter is None:
                try:
                    src = next(self._sources_iter)
                    self._curr_source = src
                    self._curr_task_iter = iter(src.get_tasks())
                except StopIteration:
                    raise StopIteration
                except Exception as e:
                    logger.warning(f'Source {src} failed on init: {e}')
                    self._curr_task_iter = None
                    continue
            try:
                task = next(self._curr_task_iter)
                if task.id in self._ids:
                    logger.warning(f'Duplicate task id {task.id} detected. Skipping...')
                    continue
                self._ids.add(task.id)
                logger.info('Task was added in queue')
                return task
            except StopIteration:
                self._curr_task_iter = None
                continue
            except Exception as e:
                logger.warning(f'Source {self._curr_source} failed during iteration: {e}')
                self._curr_task_iter = None
                continue
