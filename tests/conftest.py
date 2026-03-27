import pytest # noqa: F401
import json # noqa: F401

from src.core.models import Task
from src.core.contract import TaskSource
from src.sources.api_source import ApiSource
from src.sources.file_source import FileSource
from src.sources.gen_source import GeneratorSource
from src.receiver import TaskReceiver

class ValidSource:
    def get_tasks(self) -> list[Task]:
        return [Task(id=1, payload="Task 1")]

class InvalidSource:
    def dont_get_tasks(self):
        return None

class BrokenSource:
    def get_tasks(self) -> list[Task]:
        raise RuntimeError('Something went wrong')
