from src.models.queue import TaskQueue
from tests.conftest import MockSource


def test_empty_q():
    q = TaskQueue()
    assert len(q) == 0
    assert list(q) == []

def test_non_empty_q(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    first_pass = [task.id for task in q]
    second_pass = [task.id for task in q]
    assert first_pass == [1, 2, 3, 4]
    assert second_pass == [1, 2, 3, 4]

def test_q_get(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    assert len(q) == 4
    assert q[0].id == 1
    assert q[3].id == 4
