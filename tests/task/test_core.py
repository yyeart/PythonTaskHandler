from src.core.models import Task


def test_task_creation():
    task = Task(id=1, payload={"data": "test"})
    assert task.id == 1
    assert task.payload == {"data": "test"}
