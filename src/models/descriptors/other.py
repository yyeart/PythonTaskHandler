from src.models.descriptors.base import BaseValidator
from src.core.exceptions import ValidationError
from src.logger.setup_logger import logger


class Const(BaseValidator):
    """
    Дескриптор постоянного значения
    """
    def __set__(self, instance, value):
        # logger.info(f'Attempt to set value {value} to instance {self.name}')
        if hasattr(instance, self.private_name):
            logger.error('Set failed')
            raise ValidationError(f'constant {self.name} cannot be changed')
        setattr(instance, self.private_name, value)

    def validate(self, value):
        ...

class CreatedAt:
    """
    Дескриптор даты создания
    """
    def __get__(self, instance, owner):
        # logger.info('Attempt to get creation date')
        if instance is None:
            logger.warning(f'instance {self} does not exist')
            return self
        return instance._created_at

    def __set__(self, instance, value):
        logger.error('Attempt to set a read-only creation date failed')
        raise ValidationError('this is a read-only field')

class FullInfoDescriptor:
    """
    Non data дескриптор полной информации о задаче
    """
    def __get__(self, instance, owner):
        # logger.info('Attempt to get full info')
        if instance is None:
            logger.warning(f'instance {self} does not exist')
            return self
        info = (
            f'Task #{instance.id}: {instance.description}\n'
            f'Priority: {instance.priority}\n'
            f'Status: {instance.status}\n'
            f'Created at: {instance.created_at}'
        )
        return info
