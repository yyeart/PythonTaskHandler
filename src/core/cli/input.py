from src.core.constants import ALLOWED_STATUSES
from src.logger.setup_logger import logger


def read_status(text: str, default: str | None = None) -> str:
    """
    Считывает и валидирует статус задачи из пользовательского ввода

    :param text: Текст в консоли
    :type text: str
    :param default: Значение по умолчанию при пустом вводе
    :type default: str | None
    :returns: Статус из списка разрешенных
    :rtype: str
    """
    while True:
        status = input(text).strip()
        if status == '':
            if default is not None:
                return default
            print('Статус обязателен')
            logger.warning('Empty status input')
            continue
        if status not in ALLOWED_STATUSES:
            print(f'Неизвестный статус: {status}\n'
                    f'Разрешенные статусы: {",".join(ALLOWED_STATUSES)}')
            logger.warning(f'Invalid status input: {status}')
            continue
        return status

def read_int(
    text: str,
    default: int | None = None,
    min_val: int | None = None,
    max_val: int | None = None
) -> int:
    """
    Считывает и валидирует целое число из пользовательского ввода

    :param text: Текст в консоли
    :type text: str
    :param default: Значение по умолчанию при пустом вводе
    :type default: str | None
    :param min_val: Минимально допустимое значение
    :type min_val: int | None
    :param max_val: Максимально допустимое значение
    :type max_val: int | None
    """
    while True:
        s = input(text).strip()
        if s == '':
            if default is not None:
                return default
            print("Значение обязательно")
            logger.warning("Empty integer input")
            continue
        try:
            val = int(s)
        except ValueError:
            print("Введите целое число")
            logger.warning(f'Invalid integer input: {s}')
            continue
        if min_val is not None and val < min_val:
            print(f'Число должно быть >= {min_val}')
            logger.warning(f'Integer input below minimum: {val}')
            continue
        if max_val is not None and val > max_val:
            print(f'Число должно быть <= {max_val}')
            logger.warning(f'Integer input above maximum: {val}')
            continue

        return val
