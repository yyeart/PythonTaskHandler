from src.core.constants import JSON_PATH
from src.core.exceptions import TaskError
from src.models.task import Task
from src.logger.setup_logger import logger
from src.sources.api_source import ApiSource
from src.sources.file_source import FileSource
from src.sources.gen_source import GeneratorSource


def demo_api() -> None:
    print('-' * 40)
    print('Demonstration of data descriptors with tasks from API')

    source = ApiSource()
    print('\nAttempt to init with bad id and priority\n')
    tasks = source.get_tasks()

    if len(tasks) != 0:
        for task in tasks:
            print(f'{task.full_info}\n')
        print('\nAttempt to change a constant\n')
        target = tasks[0]
        try:
            target.id = 123
        except TaskError as e:
            print(f'Task error: {e}')
            logger.error(f'Task error: {e}')
        print('\nAttempt to set bad description\n')
        try:
            target.description = 999
        except TaskError as e:
            print(f'Task error: {e}')
            logger.error(f'Task error: {e}')
    print('\nFinal list of tasks:')
    for task in tasks:
        print(f'{task.full_info}\n')
    logger.info('Demonstration finished')

def demo_file() -> None:
    print('-' * 40)
    print('Demonstration of non-data descriptors with tasks from file')

    source = FileSource(JSON_PATH)
    tasks = source.get_tasks()

    if len(tasks) != 0:
        for task in tasks:
            print(f'{task.full_info}\n')
        target = tasks[0]
        print('Attempt to change full info of first task')
        target.full_info = 'Custom info'
        print(f'Full info now:\n{target.full_info}')
        print(f'Other fields access is unchanged:\n{target.description}')
    logger.info('Demonstration finished')

def demo_gen() -> None:
    print('-' * 40)
    print('Demonstration of properties with generated tasks')

    source = GeneratorSource(3)
    tasks = source.get_tasks()

    if len(tasks) != 0:
        for task in tasks:
            print(f'{task.full_info}\n')
        target = Task(id=50, description="Target task", priority=10)
        print('Attempt to get a calculated value')
        print(f'is_executable: {target.is_executable}')
        print('Attemp to change it')
        logger.info('Attempt to change a calculated value')
        try:
            target.is_executable = False # type: ignore[misc]
        except AttributeError as e:
            print(e)
            logger.error(e)

        print('Attempt to make forbidden transition')
        try:
            target.status = 'Done'
        except TaskError as e:
            print(f'Task error: {e}')
            logger.error(f'Task error: {e}')
        print('Attempt to make allowed transition')
        target.status = 'In_progress'

        print(f'Check if is_executable changed after status change: {target.is_executable}')
    logger.info('Demonstration finished')

def demo_read_only() -> None:
    """
    Демонстрирует работу полей доступных только для чтения

    :returns: Ничего не возвращает
    :rtype: None
    """
    print('-' * 40)
    print('Demonstration of read only fields with generated tasks')

    source = GeneratorSource(1)
    tasks = source.get_tasks()

    target = tasks[0]
    print(f'\n{target.full_info}\n')
    print('Attempt to set a read-only field')
    try:
        target.created_at = 'Right now'
    except TaskError as e:
        print(f'Task error: {e}')
        logger.error(f'Task error: {e}')
    logger.info('Demonstration finished')
