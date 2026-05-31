import pytest

from src.core.execution_exceptions import TaskExecutionError
from src.handlers.low_priority_handler import LowPriorityTaskHandler
from src.models.task import Task


@pytest.mark.asyncio
async def test_handler_success():
    task = Task(id=1, description='Task 1', priority=2)
    handler = LowPriorityTaskHandler()
    assert handler.can_handle(task)
    await handler.handle(task)
    assert task.status == 'Done'

@pytest.mark.asyncio
async def test_handler_fail():
    task = Task(id=1, description='Task 1', priority=10)
    handler = LowPriorityTaskHandler()
    assert not handler.can_handle(task)
    with pytest.raises(TaskExecutionError):
        await handler.handle(task)
    assert task.status == 'Planned'
