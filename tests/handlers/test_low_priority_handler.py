import logging

import pytest

from src.core.execution_exceptions import TaskExecutionError
from src.handlers.low_priority_handler import LowPriorityTaskHandler
from tests.conftest import DummyTask


@pytest.mark.asyncio
async def test_handler_success():
    task = DummyTask(id=1, priority=2)
    handler = LowPriorityTaskHandler()
    assert handler.can_handle(task)
    await handler.handle(task)
    assert task.status == 'Done'

@pytest.mark.asyncio
async def test_handler_fail(caplog):
    task = DummyTask(id=1, priority=10)
    handler = LowPriorityTaskHandler()
    assert not handler.can_handle(task)
    with caplog.at_level(logging.WARNING):
        with pytest.raises(TaskExecutionError):
            await handler.handle(task)
    assert 'Cannot handle task 1' in caplog.text
