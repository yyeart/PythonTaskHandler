from src.sources.api_source import ApiSource


def test_api_source():
    source = ApiSource()
    tasks = source.get_tasks()
    assert len(tasks) == 3
    assert tasks[0].id == 1
    assert isinstance(tasks[0].payload, dict)
