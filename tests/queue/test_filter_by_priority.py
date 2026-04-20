from src.models.queue import TaskQueue
from tests.conftest import MockSource


def test_filter_by_priority(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    view = q.all().filter_by_priority(10)
    assert [task.id for task in view] == [3, 4]

def test_filter_by_priority_repeat(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    view = q.all().filter_by_priority(5)
    assert [task.id for task in view] == [2, 3, 4]
    assert [task.id for task in view] == [2, 3, 4]
