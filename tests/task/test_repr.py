
from src.constants import SOURCES


def test_sources():
    assert len(SOURCES) == 3
    assert SOURCES[0].__repr__() == 'Файловый источник'
    assert SOURCES[1].__repr__() == 'Генератор'
    assert SOURCES[2].__repr__() == 'API'
