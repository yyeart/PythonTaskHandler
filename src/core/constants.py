import random

from src.sources.api_source import ApiSource
from src.sources.file_source import FileSource
from src.sources.gen_source import GeneratorSource


SOURCES = [
        FileSource("src\\sources\\input.json"),
        GeneratorSource(random.randint(3, 10)),
        ApiSource()
    ]

ALLOWED_STATUSES = ('Planned', 'In_progress', 'Done', 'Cancelled')

ALLOWED_STATUS_TRANSITIONS = {
    'Planned': ['In_progress', 'Cancelled'],
    'In_progress': ['Done', 'Cancelled'],
    'Done': [],
    'Cancelled': []
}
