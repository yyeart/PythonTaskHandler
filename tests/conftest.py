from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from src.execution.async_queue import AsyncTaskQueue
from src.models.task import Task


@dataclass
class DummyTask:
    id: int
    priority: int = 5
    status: str = 'Planned'

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

@pytest.fixture
def sample_tasks():
    return [
        Task(id=1, description="Task 1", priority=1, status='Planned'),
        Task(id=2, description="Task 2", priority=5, status='In_progress'),
        Task(id=3, description="Task 3", priority=10, status='Done'),
        Task(id=4, description="Task 4", priority=10, status='In_progress')
    ]

@pytest.fixture
def queue():
    return AsyncTaskQueue(2)

class DummyHandler:
    def __init__(self, name, can_handle = True):
        self.name = name
        self._can_handle = can_handle
        self.handle = AsyncMock()

    def can_handle(self, task):
        return self._can_handle
