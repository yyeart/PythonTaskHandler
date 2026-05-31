import logging
from unittest.mock import call

import pytest

from src.core.execution_exceptions import ExecutionError
from src.execution.executor import TaskExecutor
from src.models.task import Task
from tests.conftest import DummyHandler


@pytest.mark.asyncio
async def test_executor_processes_tasks():
    handler = DummyHandler(name='universal', can_handle=True)
    executor = TaskExecutor(handlers=[handler], worker_count=1)
    task1 = Task(id=1, description='Task 1', priority=5)
    task2 = Task(id=2, description='Task 2', priority=6)
    await executor.start()
    await executor.submit_task(task1)
    await executor.submit_task(task2)
    await executor.stop()
    assert handler.handle.await_count == 2
    handler.handle.assert_has_awaits([call(task1), call(task2)])
    assert executor.stats.started == 2
    assert executor.stats.completed == 2
    assert executor.stats.failed == 0
    assert executor.stats.skipped == 0

@pytest.mark.asyncio
async def test_executor_resolves_first_matching_handler():
    task = Task(id=1, description='Task 1', priority=9)
    handler_low = DummyHandler(name='low', can_handle=False)
    handler_high = DummyHandler(name='high', can_handle=True)
    executor = TaskExecutor(handlers=[handler_low, handler_high], worker_count=1)
    await executor.start()
    await executor.submit_task(task)
    await executor.stop()
    handler_low.handle.assert_not_called()
    handler_high.handle.assert_awaited_once_with(task)

@pytest.mark.asyncio
async def test_executor_skips_when_handler_not_found(caplog):
    task = Task(id=1, description='Task 1', priority=5)
    bad_handler = DummyHandler(name='bad', can_handle=False)
    executor = TaskExecutor(handlers=[bad_handler], worker_count=1)
    with caplog.at_level(logging.WARNING):
        await executor.start()
        await executor.submit_task(task)
        await executor.stop()
    assert 'skipped task 1' in caplog.text
    assert task.status == 'Planned'
    assert executor.stats.skipped == 1

@pytest.mark.asyncio
async def test_executor_marks_failed_task_on_handler_exception():
    task = Task(id=1, description='Task 1', priority=5)
    handler = DummyHandler(name='broken', can_handle=True)
    handler.handle.side_effect = RuntimeError('fail')
    executor = TaskExecutor(handlers=[handler], worker_count=1)
    await executor.start()
    await executor.submit_task(task)
    await executor.stop()
    assert task.status == 'Failed'
    assert executor.stats.failed == 1
    assert executor.stats.completed == 0

def test_executor_rejects_invalid_worker_count():
    handler = DummyHandler(name='universal', can_handle=True)
    with pytest.raises(ExecutionError):
        TaskExecutor(handlers=[handler], worker_count=0)

def test_executor_rejects_non_handler_object():
    with pytest.raises(ExecutionError):
        TaskExecutor(handlers=[object()], worker_count=1)
