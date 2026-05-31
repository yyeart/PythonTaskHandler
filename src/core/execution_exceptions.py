class ExecutionError(Exception):
    """Класс общей ошибки при работе с TaskExecutor"""
    ...

class HandlerNotFoundError(ExecutionError):
    """
    Класс ошибки, при которой задача не может быть обработана ни одним Handler
    """
    ...

class QueueClosedError(ExecutionError):
    """Класс ошибки при запрещенных действиях с закрытой очередью"""
    ...

class TaskExecutionError(ExecutionError):
    """Класс ошибки выполнения задачи"""
    ...
