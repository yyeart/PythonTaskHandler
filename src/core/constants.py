ALLOWED_STATUSES = ('Planned', 'In_progress', 'Done', 'Cancelled')

ALLOWED_STATUS_TRANSITIONS = {
    'Planned': ['In_progress', 'Cancelled'],
    'In_progress': ['Done', 'Cancelled'],
    'Done': [],
    'Cancelled': []
}
