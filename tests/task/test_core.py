from src.models.task import Task


def test_task_creation():
    task = Task(id=666, description='test desc', priority=5)
    assert task.id == 666
    assert task.description == 'test desc'
    assert task.priority == 5
    assert task.status == 'Planned'
