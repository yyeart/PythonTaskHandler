from src.models.descriptors.base import BaseValidator
from src.core.exceptions import ValidationError
from src.logger.setup_logger import logger


class NotEmptyString(BaseValidator):
    """
    Строковый дескриптор проверяющий минимальную длину строки
    """
    def validate(self, value):
        if not isinstance(value, str):
            logger.error('Validation failed')
            raise ValidationError(f'{self.name} must be a string, got {type(value).__name__}')
        if len(value) < 3:
            logger.error('Validation failed')
            raise ValidationError(f'{self.name} must have at least 3 characters')
