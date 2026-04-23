from src.models.queue import TaskQueue
from tests.conftest import MockSource


def test_filter_by_status(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    view = q.filter_by_status("Planned")
    results = list(view)
    assert len(results) == 1
    assert results[0].status == 'Planned'

def test_filter_by_status_repeat(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource(sample_tasks))
    view = q.filter_by_status('Done')
    assert [task.id for task in view] == [3]
    assert [task.id for task in view] == [3]
