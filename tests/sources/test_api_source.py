from src.models.task import Task
from src.sources.api_source import ApiSource


def test_api_source():
    Task._clear_ids()
    source = ApiSource()
    tasks = source.get_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
