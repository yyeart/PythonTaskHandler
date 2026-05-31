# from functools import wraps

# from src.logger.setup_logger import logger


# def catch_empty(func):
#     @wraps(func)
#     async def wrapper(self, *args, **kwargs):
#         if not self._prepared_tasks:
#             logger.warning("Empty queue access attempted")
#             print('Задачи не найдены. Сначала добавьте источники\n')
#             return
#         return await func(self, *args, **kwargs)
#     return wrapper
