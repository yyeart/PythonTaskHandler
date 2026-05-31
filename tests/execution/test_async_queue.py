import asyncio

import pytest

from src.core.execution_exceptions import QueueClosedError
from src.models.task import Task


@pytest.mark.asyncio
async def test_put_and_get_success(queue):
    task = Task(id=1, description='Task 1', priority=1)
    await queue.put(task)
    retrieved_task = await queue.get()
    assert retrieved_task == task
    assert retrieved_task.id == 1
    queue.task_done()

@pytest.mark.asyncio
async def test_queue_maxsize_blocks_put(queue):
    await queue.put(Task(id=1, description='Task 1', priority=1))
    await queue.put(Task(id=2, description='Task 2', priority=2))
    put_task = asyncio.create_task(queue.put(Task(id=3, description='Task 3', priority=3)))
    await asyncio.sleep(0.01)
    assert not put_task.done()
    await queue.get()
    queue.task_done()
    await asyncio.wait_for(put_task, timeout=1)
    assert put_task.done()

@pytest.mark.asyncio
async def test_put_to_closed_queue(queue):
    queue.close()
    with pytest.raises(QueueClosedError):
        await queue.put(Task(id=1, description='Task 1', priority=1))
    with pytest.raises(QueueClosedError):
        await queue.get()
    with pytest.raises(QueueClosedError):
        await queue.get()

@pytest.mark.asyncio
async def test_get_from_closed_queue(queue):
    task = Task(id=1, description='Task 1', priority=1)
    await queue.put(task)
    queue.close()
    retrieved_task = await queue.get()
    assert retrieved_task == task
    queue.task_done()
    with pytest.raises(QueueClosedError):
        await queue.get()
    with pytest.raises(QueueClosedError):
        await queue.get()

@pytest.mark.asyncio
async def test_join_and_task_done(queue):
    await queue.put(Task(id=1, description='Task 1', priority=1))
    join_task = asyncio.create_task(queue.join())
    await asyncio.sleep(0.01)
    assert not join_task.done()
    await queue.get()
    queue.task_done()
    await asyncio.wait_for(join_task, timeout=1)
    assert join_task.done()
