import logging

import pytest

from src.execution.stats import ExecutionStats
from src.execution.resources import ExecutionSession


@pytest.mark.asyncio
async def test_execution_session_success(caplog):
    session_id = 'w1-t1'
    stats = ExecutionStats()
    with caplog.at_level(logging.INFO):
        async with ExecutionSession(session_id, stats) as session:
            assert isinstance(session, ExecutionSession)
            assert session.session_id == session_id
            assert stats.started == 1
            assert f'Session {session_id} started' in caplog.text
    assert stats.completed == 1
    assert stats.failed == 0
    assert stats.active_sessions == 0
    assert f'Session {session_id} finished' in caplog.text
    assert 'crashed with error' not in caplog.text

@pytest.mark.asyncio
async def test_execution_session_error(caplog):
    session_id = 'w9-t99'
    stats = ExecutionStats()
    with caplog.at_level(logging.INFO):
        with pytest.raises(ZeroDivisionError):
            async with ExecutionSession(session_id, stats):
                1 / 0
    assert stats.started == 1
    assert stats.completed == 0
    assert stats.failed == 1
    assert stats.active_sessions == 0
    assert f'Session {session_id} started' in caplog.text
    assert f'Session {session_id} crashed with error: division by zero' in caplog.text
    assert f'Session {session_id} finished' not in caplog.text
