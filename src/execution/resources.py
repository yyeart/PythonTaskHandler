import asyncio

from src.execution.stats import ExecutionStats
from src.logger.setup_logger import logger


class ExecutionSession:
    """Асинхронный контекстный менеджер, отслеживающий статистику"""
    def __init__(self, session_id: str, stats: ExecutionStats) -> None:
        self.session_id = session_id
        self.stats = stats

    async def __aenter__(self) -> "ExecutionSession":
        """Регистрирует начало сессии"""
        logger.info(f'Session {self.session_id} started')
        self.stats.add_started()
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        """Завершает сессию и обновляет статистику успехов и фейлов"""
        await asyncio.sleep(0.1)
        if exc is not None:
            logger.error(f'Session {self.session_id} crashed with error: {exc}')
            self.stats.add_failed()
            return False
        self.stats.add_completed()
        logger.info(f'Session {self.session_id} finished')
        logger.info(f'Active sessions left: {self.stats.active_sessions}')
        return True
