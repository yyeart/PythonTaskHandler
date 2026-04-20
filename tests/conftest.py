import pytest # noqa: F401

from src.models.task import Task


class ValidSource:
    def get_tasks(self):
        return [Task(id=1, description="Task 1", priority=1)]

class InvalidSource:
    def dont_get_tasks(self):
        return None

class BrokenSource:
    def get_tasks(self):
        raise RuntimeError('Something went wrong')

class MockSource:
    def __init__(self, tasks) -> None:
        self.tasks = tasks

    def get_tasks(self):
        for task in self.tasks:
            yield task

    def __str__(self) -> str:
        return "MockSource"

@pytest.fixture(autouse=True)
def clear_ids():
    Task._clear_ids()
    yield

@pytest.fixture
def sample_tasks():
    return [
        Task(id=1, description="Task 1", priority=1, status='Planned'),
        Task(id=2, description="Task 2", priority=5, status='In_progress'),
        Task(id=3, description="Task 3", priority=10, status='Done'),
        Task(id=4, description="Task 4", priority=10, status='In_progress')
    ]
