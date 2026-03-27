from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Task:
    """Структура данных задачи"""
    id: int
    payload: Any
