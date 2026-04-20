from src.models.queue import TaskQueue
from src.models.task import Task
from tests.conftest import MockSource


def test_broken_source():
    class BrokenSource:
        def get_tasks(self):
            yield Task(id=1, description="Task")
            raise RuntimeError("Error")

    q = TaskQueue()
    q.add_source(BrokenSource())
    assert len(q) == 1
    assert [task.id for task in q] == [1]

def test_many_sources(sample_tasks):
    q = TaskQueue()
    q.add_source(MockSource([sample_tasks[0]]))
    q.add_source(MockSource([sample_tasks[1]]))
    assert len(q) == 2
    assert [task.id for task in q] == [1, 2]
