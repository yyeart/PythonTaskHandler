import json

from src.models.task import Task
from src.sources.file_source import FileSource


def test_file_source(tmp_path):
    Task._clear_ids()
    d = tmp_path / "subdir1"
    d.mkdir()
    f = d / "tasks.json"
    f.write_text(json.dumps([{"id": 1, "description": "test desc", "priority": 5}]))

    source = FileSource(str(f))
    tasks = source.get_tasks()

    assert len(tasks) == 1
    assert tasks[0].id == 1

def test_file_source_not_found():
    Task._clear_ids()
    source = FileSource("fake_path.json")
    tasks = source.get_tasks()
    assert len(tasks) == 0

def test_file_source_invalid_json(tmp_path):
    Task._clear_ids()
    f = tmp_path / "wrong.json"
    f.write_text("not json")

    source = FileSource(str(f))
    tasks = source.get_tasks()
    assert len(tasks) == 0

def test_file_source_key_error(tmp_path):
    Task._clear_ids()
    f = tmp_path / 'bad_keys.json'
    f.write_text(json.dumps([{"invalid_key": "value"}]))
    source = FileSource(str(f))
    tasks = source.get_tasks()
    assert len(tasks) == 0
