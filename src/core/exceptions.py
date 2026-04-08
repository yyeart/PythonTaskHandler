class TaskError(Exception):
    """
    Класс общей ошибки при работе с Task
    """
    ...

class ValidationError(TaskError):
    """
    Класс ошибки валидации того или иного поля Task
    """
    ...

class StateError(TaskError):
    """
    Класс ошибки перехода статусов Task
    """
    ...
    