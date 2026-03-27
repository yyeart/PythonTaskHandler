import json

from src.sources.file_source import FileSource


def test_file_source(tmp_path):
    d = tmp_path / "subdir1"
    d.mkdir()
    f = d / "tasks.json"
    f.write_text(json.dumps([{"id": 10, "payload": "file_payload"}]))

    source = FileSource(str(f))
    tasks = source.get_tasks()

    assert len(tasks) == 1
    assert tasks[0].id == 10

def test_file_source_not_found():
    source = FileSource("fake_path.json")
    tasks = source.get_tasks()
    assert len(tasks) == 0

def test_file_source_invalid_json(tmp_path):
    f = tmp_path / "wrong.json"
    f.write_text("not json")

    source = FileSource(str(f))
    tasks = source.get_tasks()
    assert len(tasks) == 0

def test_file_source_key_error(tmp_path):
    f = tmp_path / 'bad_keys.json'
    f.write_text(json.dumps([{"invalid_key": "value"}]))
    source = FileSource(str(f))
    tasks = source.get_tasks()
    assert len(tasks) == 0
