from pathlib import Path


ALLOWED_STATUSES = ('Planned', 'In_progress', 'Done', 'Cancelled')

ALLOWED_STATUS_TRANSITIONS = {
    'Planned': ['In_progress', 'Cancelled'],
    'In_progress': ['Done', 'Cancelled'],
    'Done': [],
    'Cancelled': []
}

BASE_DIR = Path(__file__).resolve().parent.parent

JSON_PATH = BASE_DIR / 'sources' / 'input.json'
