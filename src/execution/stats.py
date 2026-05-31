class ExecutionStats:
    def __init__(self) -> None:
        self.started: int = 0
        self.completed: int = 0
        self.failed: int = 0
        self.skipped: int = 0
        self._active_sessions: int = 0

    @property
    def active_sessions(self) -> int:
        return self._active_sessions

    def add_started(self) -> None:
        self.started += 1
        self._active_sessions += 1

    def add_completed(self) -> None:
        self.completed += 1
        self._active_sessions -= 1

    def add_failed(self) -> None:
        self.failed += 1
        self._active_sessions -= 1

    def add_skipped(self) -> None:
        self.skipped += 1

    def get_summary(self) -> str:
        return (
            f'--- Итог: ---\n'
            f'Всего получено: {self.started + self.skipped}\n'
            f'Запущено: {self.started}\n'
            f'Успешно завершено: {self.completed}\n'
            f'Зафейлены: {self.failed}\n'
            f'Пропущено: {self.skipped}\n'
            f'Активных в моменте: {self._active_sessions}\n'
        )
