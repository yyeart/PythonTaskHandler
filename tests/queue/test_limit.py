from src.models.queue import TaskQueue
from tests.conftest import MockSource


def test_limit_zero(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    assert len(list(q.limit(0))) == 0

def test_limit_more_than_exists(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    assert len(list(q.limit(100))) == 4

def test_limit_repeat(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    view = q.limit(2)
    assert [task.id for task in view] == [1, 2]
    assert [task.id for task in view] == [1, 2]
