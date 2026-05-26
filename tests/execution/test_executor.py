import logging

import pytest

from src.execution.executor import TaskExecutor
from tests.conftest import DummyHandler, DummyTask


@pytest.mark.asyncio
async def test_executor_success():
    task1 = DummyTask(id=1)
    task2 = DummyTask(id=2)
    handler = DummyHandler(name='uni_handler', can_handle=True)
    executor = TaskExecutor(handlers=[handler])
    await executor.run([task1, task2])
    assert handler.handle.call_count == 2
    handler.handle.assert_any_call(task1)
    handler.handle.assert_any_call(task2)

@pytest.mark.asyncio
async def test_executor_resolve_handler_success():
    task = DummyTask(id=1, priority=9, status='Planned')
    handler_low = DummyHandler(name='low', can_handle=False)
    handler_high = DummyHandler(name='high', can_handle=True)
    executor = TaskExecutor(handlers=[handler_high, handler_low])
    await executor.run([task])
    handler_low.handle.assert_not_called()
    handler_high.handle.assert_called_once_with(task)

@pytest.mark.asyncio
async def test_executor_handler_not_found(caplog):
    task = DummyTask(id=1)
    bad_handler = DummyHandler(name='bad', can_handle=False)
    executor = TaskExecutor(handlers=[bad_handler])
    with caplog.at_level(logging.ERROR):
        await executor.run([task])
    assert 'No handler found for task 1' in caplog.text

@pytest.mark.asyncio
async def test_executor_worker_resistance():
    bad_task = DummyTask(id=1)
    normal_task = DummyTask(id=2)
    handler = DummyHandler(name='uni_handler')
    handler.handle.side_effect = [RuntimeError('fail'), None]
    executor = TaskExecutor(handlers=[handler])
    await executor.run([bad_task, normal_task])
    assert handler.handle.call_count == 2
    handler.handle.assert_any_call(bad_task)
    handler.handle.assert_any_call(normal_task)

@pytest.mark.asyncio
async def test_submit_tasks():
    task1 = DummyTask(id=1)
    task2 = DummyTask(id=2)
    executor = TaskExecutor(handlers=[])
    await executor.submit_tasks(executor.execution_queue, [task1, task2])
    assert await executor.execution_queue.get() == task1
    assert await executor.execution_queue.get() == task2
