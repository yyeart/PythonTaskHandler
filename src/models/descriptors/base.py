from abc import ABC, abstractmethod

from src.logger.setup_logger import logger


class BaseValidator(ABC):
    """
    Базовый валидатор, от которого наследуются почти все остальные дескрипторы
    """
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        # logger.info(f'Attempt to get instance {self.name}')
        if instance is None:
            logger.warning(f'Instance {self} does not exist')
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        # logger.info(f'Attempt to set value {value} to instance {self.name}')
        self.validate(value)
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        """Метод для переопределения в конкретных дескрипторах"""
        ...
