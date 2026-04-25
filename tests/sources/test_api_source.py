from src.sources.api_source import ApiSource


def test_api_source():
    source = ApiSource()
    tasks = list(source.get_tasks())
    assert len(tasks) == 3
    assert tasks[0].id == 1
