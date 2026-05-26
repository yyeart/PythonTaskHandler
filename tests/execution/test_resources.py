import logging

import pytest

from src.execution.resources import ExecutionSession


@pytest.mark.asyncio
async def test_execution_session_success(caplog):
    session_id = 1
    with caplog.at_level(logging.INFO):
        async with ExecutionSession(session_id) as session:
            assert isinstance(session, ExecutionSession)
            assert session.session_id == session_id
            assert f'Session {session_id} started' in caplog.text
    assert f'Session {session_id} finished' in caplog.text
    assert 'crashed with error' not in caplog.text

@pytest.mark.asyncio
async def test_execution_session_error(caplog):
    session_id = 99
    with caplog.at_level(logging.INFO):
        with pytest.raises(ZeroDivisionError):
            async with ExecutionSession(session_id):
                1 / 0
    assert f'Session {session_id} started' in caplog.text
    assert f'Session {session_id} crashed with error: division by zero' in caplog.text
    assert f'Session {session_id} finished' in caplog.text
