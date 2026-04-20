from src.models.queue import TaskQueue
from tests.conftest import MockSource


def test_chain(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    result = list(q.all().filter_by_status('In_progress').filter_by_priority(5).limit(1))
    assert len(result) == 1
    assert result[0].id == 2

def test_chain_order(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    result1 = list(q.all().limit(1).filter_by_priority(10))
    result2 = list(q.all().filter_by_priority(10).limit(1))
    assert len(result1) == 0
    assert len(result2) == 1
