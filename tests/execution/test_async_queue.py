import pytest
import asyncio

from src.core.execution_exceptions import QueueClosedError
from tests.conftest import DummyTask


@pytest.mark.asyncio
async def test_put_and_get_success(queue):
    task = DummyTask(id=1)
    await queue.put(task)
    retrieved_task = await queue.get()
    assert retrieved_task == task
    assert retrieved_task.id == 1

@pytest.mark.asyncio
async def test_queue_maxsize_blocks_put(queue):
    await queue.put(DummyTask(id=1))
    await queue.put(DummyTask(id=2))
    put_task = asyncio.create_task(queue.put(DummyTask(id=3)))
    await asyncio.sleep(0.01)
    assert not put_task.done()
    await queue.get()
    await asyncio.sleep(0.01)
    assert put_task.done()

@pytest.mark.asyncio
async def test_put_to_closed_queue(queue):
    queue.close()
    with pytest.raises(QueueClosedError):
        await queue.put(DummyTask(id=1))

@pytest.mark.asyncio
async def test_get_from_closed_queue(queue):
    task = DummyTask(id=1)
    await queue.put(task)
    queue.close()
    retrieved_task = await queue.get()
    assert retrieved_task == task

@pytest.mark.asyncio
async def test_join_and_task_done(queue):
    await queue.put(DummyTask(id=1))
    join_task = asyncio.create_task(queue.join())
    await asyncio.sleep(0.01)
    assert not join_task.done()
    await queue.get()
    queue.task_done()
    await asyncio.sleep(0.01)
    assert join_task.done()
