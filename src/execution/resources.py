import asyncio

from src.logger.setup_logger import logger


class ExecutionSession:
    def __init__(self, session_id: int) -> None:
        self.session_id = session_id

    async def __aenter__(self) -> "ExecutionSession":
        logger.info(f'Session {self.session_id} started')
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await asyncio.sleep(0.1)
        if exc is not None:
            logger.error(f'Session {self.session_id} crashed with error: {exc}')
        logger.info(f'Session {self.session_id} finished')
