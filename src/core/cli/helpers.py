from functools import wraps
from typing import Any, Callable

from src.logger.setup_logger import logger


def not_empty(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор, который запрещает выполнять команды с пустой очередью"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        queue = args[1]
        if len(queue) > 0:
            func(*args, **kwargs)
        else:
            logger.warning("Empty queue access attempted")
            print('Очередь пуста!\n')
    return wrapper
