from src.models.task_view import TaskView
from src.logger.setup_logger import logger


class TaskQueue: # TODO АННОТАЦИИ ДОБАВИТЬ!!!
    def __init__(self):
        self.__tasks = []

    def add_source(self, source: object):
        init_count = len(self.__tasks)
        try:
            for task in source.get_tasks(): # type: ignore[attr-defined]
                self.__tasks.append(task)
            logger.info(f'Loaded {len(self.__tasks)-init_count} tasks from {source}')
        except Exception as e:
            logger.error(f'{source} raised an exception: {e}')

    def __iter__(self):
        return iter(self.__tasks)

    def __len__(self) -> int:
        return len(self.__tasks)

    def __getitem__(self, index: int):
        return self.__tasks[index]

    def all(self):
        return TaskView(lambda: iter(self.__tasks))
