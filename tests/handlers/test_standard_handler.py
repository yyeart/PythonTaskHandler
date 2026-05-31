import pytest

from src.core.execution_exceptions import TaskExecutionError
from src.handlers.standard_handler import StandardTaskHandler
from src.models.task import Task


@pytest.mark.asyncio
async def test_handler_success():
    task = Task(id=1, description='Task 1', priority=5)
    handler = StandardTaskHandler()
    assert handler.can_handle(task)
    await handler.handle(task)
    assert task.status == 'Done'

@pytest.mark.asyncio
async def test_handler_fail():
    task = Task(id=1, description='Task 1', priority=1)
    handler = StandardTaskHandler()
    assert not handler.can_handle(task)
    with pytest.raises(TaskExecutionError):
        await handler.handle(task)
    assert task.status == 'Planned'
