from pathlib import Path

from src.sources.file_source import FileSource


base_dir = Path("tests") / "files"

def test_file_source():
    source = FileSource(base_dir / "input.json")
    tasks = list(source.get_tasks())

    assert len(tasks) == 1
    assert tasks[0].id == 1

def test_file_source_not_found():
    source = FileSource("fake_path.json")
    tasks = list(source.get_tasks())
    assert len(tasks) == 0

def test_file_source_invalid_json():
    source = FileSource(base_dir / "not_json.json")
    tasks = list(source.get_tasks())
    assert len(tasks) == 0

def test_file_source_key_error():
    source = FileSource(base_dir / "bad_key.json")
    tasks = list(source.get_tasks())
    assert len(tasks) == 0
