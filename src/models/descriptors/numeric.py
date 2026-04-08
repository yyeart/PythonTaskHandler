from src.models.descriptors.base import BaseValidator
from src.core.exceptions import ValidationError
from src.logger.setup_logger import logger


class IntRange(BaseValidator):
    """
    Числовой дескриптор проверяющий нахождение числа в диапазоне
    """
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value):
        if not isinstance(value, int):
            logger.error('Validation failed')
            raise ValidationError(f'{self.name} must be an integer, got {type(value).__name__}')
        if (self.min_val is not None and self.max_val is not None
            and not (self.min_val <= value <= self.max_val)):
            logger.error('Validation failed')
            raise ValidationError(f'{self.name} must be in [{self.min_val}, {self.max_val}]')
