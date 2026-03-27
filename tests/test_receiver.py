from src.receiver import TaskReceiver
from tests.conftest import BrokenSource, InvalidSource, ValidSource


def test_receiver_filter():
    receiver = TaskReceiver()
    sources = [ValidSource(), InvalidSource()]
    receiver.receive_tasks(sources)
    tasks = receiver.get_received_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1

def test_receiver_error_handling():
    receiver = TaskReceiver()
    sources = [BrokenSource(), ValidSource()]

    receiver.receive_tasks(sources)

    assert len(receiver.get_received_tasks()) == 1
