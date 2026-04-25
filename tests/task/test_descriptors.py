import pytest # type: ignore [import-not-found]

from src.core.exceptions import StateError, TaskError
from src.models.task import Task


def test_const_protection():
    t = Task(id=1, description='test', priority=1)
    with pytest.raises(TaskError):
        t.id = 2

def test_non_empty_string():
    with pytest.raises(TaskError):
        Task(id=1, description="", priority=1)

def test_int_range():
    with pytest.raises(TaskError):
        Task(id=1, description='1231313', priority=123)
    with pytest.raises(TaskError):
        Task(id=1, description='123131313', priority=0)

def test_status_transitions():
    t = Task(id=1, description='1231313', priority=1)
    t.status = 'In_progress'
    assert t.status == 'In_progress'
    with pytest.raises(StateError):
        t.status = 'Planned'

def test_status_validation():
    t = Task(id=1, description='asdada', priority=2)
    with pytest.raises(ValueError):
        t.status = 'Gotovo)))'

def test_is_executable():
    t = Task(id=1, description='Test', priority=1)
    assert t.is_executable
    t.status = 'In_progress'
    assert not t.is_executable

def test_read_only():
    t = Task(id=1, description='test', priority=1)
    with pytest.raises(TaskError):
        t.created_at = 'right now'
