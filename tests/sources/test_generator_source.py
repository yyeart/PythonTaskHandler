from unittest.mock import patch

from src.models.task import Task
from src.sources.gen_source import GeneratorSource


def test_generator_source():
    source = GeneratorSource(5)
    tasks = list(source.get_tasks())
    assert isinstance(tasks, list)
    if(len(tasks) > 0):
        assert isinstance(tasks[0], Task)

def test_generator_zero_tasks():
    source = GeneratorSource(0)
    assert len(list(source.get_tasks())) == 0

def test_generator_exception():
    source = GeneratorSource(5)
    with patch('random.randint', side_effect=Exception("Mock Error")):
        tasks = list(source.get_tasks())
        assert len(tasks) == 0
