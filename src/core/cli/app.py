from src.core.cli.helpers import not_empty
from src.core.cli.input import read_int, read_status
from src.core.constants import JSON_PATH
from src.core.contract import TaskSource
from src.core.exceptions import TaskError
from src.demonstration import demo_api, demo_file, demo_gen, demo_read_only
from src.models.queue import TaskQueue
from src.models.task import Task
from src.receiver import TaskReceiver
from src.logger.setup_logger import logger
from src.sources.api_source import ApiSource
from src.sources.file_source import FileSource
from src.sources.gen_source import GeneratorSource


class CommandLineInterface:
    """
    Класс, представляющий собой интерактивный CLI для пользователя
    """
    def __init__(self, gen_task_cnt: int = 3) -> None:
        self._queue = TaskQueue()
        self._sources: list[TaskSource] = [
            ApiSource(),
            FileSource(JSON_PATH),
            GeneratorSource(gen_task_cnt)
        ]

    def _demo_descriptors(self) -> None:
        """
        Функция для демонстрации работы дескрипторов и источников задач по выбору
        """
        print(
            '1. Data дескрипторы с задачами из API\n'
            '2. Non-data дескрипторы с задачами из файла\n'
            '3. Property-свойства с задачами из генератора\n'
            '4. Read-only поля с задачами из ...'
        )
        match (_ := input('Вариант: ')):
            case '1':
                demo_api()

            case '2':
                demo_file()

            case '3':
                demo_gen()

            case '4':
                demo_read_only()

            case _:
                print('Неизвестный вариант')
        Task._clear_ids()

    def _receive(self, sources: list[TaskSource]) -> None:
        """
        Функция для сбора задач из всех источников

        :param sources: Список объектов источников
        :type sources: list[object]
        """
        receiver = TaskReceiver()

        logger.info('Начало сбора задач...')
        receiver.receive_tasks(sources)
        result = receiver.get_received_tasks()
        logger.info(f'Сбор завершен. Всего задач: {len(result)}')

        print('Список задач:')
        for task in result:
            print(f'{task.full_info}\n')

    def _validation_test(self) -> None:
        """
        Функция для создания задачи по параметрам пользователя
        """
        task = None
        while task is None:
            try:
                print('Инициализация задачи')
                task_id = read_int('Введите ID: ', min_val=1)
                task_desc = input('Введите описание: ')
                task_priority = read_int('Задайте приоритет: ', min_val=1, max_val=10)
                task_status = read_status('Задайте статус (Enter - Planned): ',
                                                default='Planned')

                task = Task(id=task_id, description=task_desc,
                            priority=task_priority, status=task_status if task_status else None)
                print('Задача прошла валидацию')
                print(task.full_info)
            except (TaskError, ValueError) as e:
                print(f'Ошибка валидации: {e}')
                logger.warning(f'Attempt to create a task failed: {e}')

    def _receive_in_queue(self, queue: TaskQueue) -> None:
        """
        Функция добавления задач из всех источников в очередь queue

        :param queue: Очередь
        :type queue: TaskQueue
        """
        for src in self._sources:
            queue.add_source(src)
        logger.info(f'{len(queue)} tasks loaded in queue')

    @not_empty
    def _print_queue(self, queue: TaskQueue) -> None:
        """Печатает все задачи из очереди"""
        print('Список задач:')
        for task in queue:
            print(f'{task.full_info}\n')

    @not_empty
    def _print_limited_queue(self, queue: TaskQueue, limit: int) -> None:
        """Печатает {limit} задач из очереди"""
        for task in queue.all().limit(limit):
            print(f'{task.full_info}\n')

    @not_empty
    def _filter_queue_priority(self, queue: TaskQueue, priority: int, limit: int) -> None:
        """Фильтрует очередь по приоритету"""
        view = queue.all().filter_by_priority(priority).limit(limit)
        for task in view:
            print(f'{task.full_info}\n')

    @not_empty
    def _filter_queue_status(self, queue: TaskQueue, status: str, limit: int) -> None:
        """Фильтрует очередь по статусу"""
        view = queue.all().filter_by_status(status).limit(limit)
        for task in view:
            print(f'{task.full_info}\n')

    def _queue_ops(self) -> None:
        """Функция для выбора операции над очередью задач"""
        text = (
            '1. Загрузить задачи из источников в очередь\n'
            '2. Вывести все задачи\n'
            '3. Вывести задачи по статусу\n'
            '4. Вывести задачи по приоритету\n'
            '5. Вывести первые n задач\n'
            '0. Выход в главное меню'
        )
        print(text)

        while (cin := input('Вариант: ').lower()) not in ['exit', '0']:
            match(cin):
                case '1':
                    logger.info('Load in queue requested')
                    self._receive_in_queue(self._queue)
                    print(text)

                case '2':
                    self._print_queue(self._queue)
                    print(text)

                case '3':
                    status = read_status('Введите статус для фильтрации (Enter - In_progress): ',
                                               default="In_progress")
                    limit = read_int('Сколько задач вывести? (Enter - Все): ',
                                           default=len(self._queue), min_val=0)
                    logger.info(f'Filter by status "{status}" requested (limit={limit})')
                    self._filter_queue_status(self._queue, status, limit)
                    print(text)

                case '4':
                    priority = read_int('Введите приоритет для фильтрации (Enter - 1): ',
                                              default=1, min_val=1, max_val=10)
                    limit = read_int('Сколько задач вывести? (Enter - Все): ',
                                           default=len(self._queue), min_val=0)
                    logger.info(f'Filter by priority "{priority}" requested (limit={limit})')
                    self._filter_queue_priority(self._queue, priority, limit)
                    print(text)

                case '5':
                    limit = read_int('Введите n: ', min_val=0)
                    logger.info(f'Queue limited by {limit} requested')
                    self._print_limited_queue(self._queue, limit)
                    print(text)

                case _:
                    logger.warning("Unknown user choice")
                    print('Неизвестный вариант')
                    print(text)

    def start_cli(self) -> None:
        """
        Основная функция CLI
        """
        text = (
            '1. Запустить авто-демонстрацию работы дескрипторов\n'
            '2. Загрузить задачи из всех источников\n'
            '3. Интерактивная проверка валидации\n'
            '4. Операции с очередью задач\n'
            '0. Выход'
        )
        print(text)
        while (cin := input('Вариант: ').lower()) not in ['exit', '0']:
            match(cin):
                case '1':
                    logger.info("Demonstration menu opened")
                    self._demo_descriptors()
                    print(text)

                case '2':
                    logger.info("Load tasks from all sourced requested")
                    self._receive(self._sources)
                    print(text)

                case '3':
                    logger.info("Validation test opened")
                    self._validation_test()
                    print(text)

                case '4':
                    logger.info("Queue menu opened")
                    self._queue_ops()
                    print(text)

                case _:
                    logger.warning("Unknown user choice")
                    print('Неизвестный вариант')
                    print(text)
