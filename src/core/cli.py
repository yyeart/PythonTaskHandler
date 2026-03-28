from src.core.exceptions import TaskError
from src.demonstration import demo_api, demo_file, demo_gen, demo_read_only
from src.models.task import Task
from src.receiver import TaskReceiver
from src.logger.setup_logger import logger
from src.sources.api_source import ApiSource
from src.sources.file_source import FileSource
from src.sources.gen_source import GeneratorSource


class CommandLineInterface:
    def _demo_descriptors(self):
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
                print('Неизвенстый вариант')

    def _receive(self, sources: list[object]):
        receiver = TaskReceiver()

        logger.info('Начало сбора задач...')
        receiver.receive_tasks(sources)
        result = receiver.get_received_tasks()
        logger.info(f'Сбор завершен. Всего задач: {len(result)}')

        print('Список задач:')
        for task in result:
            print(f'{task.full_info}\n')

    def _validation_test(self):
        task = None
        while task is None:
            try:
                print('Инициализация задачи')
                task_id = int(input('Введите ID: '))
                task_desc = input('Введите описание: ')
                task_priority = int(input('Задайте приоритет: '))
                task_status = input('Задайте статус (можно оставить пустым): ')

                task = Task(id=task_id, description=task_desc,
                            priority=task_priority, status=task_status if task_status else None)
                print('Задача прошла валидацию')
                print(task.full_info)
            except (TaskError, ValueError) as e:
                print(f'Validator error: {e}')
                logger.warning(f'Attempt to create a task failed: {e}')

    def start_cli(self) -> None:
        text = (
            '1. Запустить авто-демонстрацию работы дескрипторов\n'
            '2. Загрузить задачи из всех источников\n'
            '3. Интерактивная проверка валидации\n'
            '0. Выход'
        )
        print(text)
        while (cin := input('Вариант: ').lower()) not in ['exit', '0']:
            match(cin):
                case '1':
                    self._demo_descriptors()
                    print(text)

                case '2':
                    sources = [
                        ApiSource(),
                        FileSource("src\\sources\\input.json"),
                        GeneratorSource(2)
                    ]
                    self._receive(sources)
                    print(text)

                case '3':
                    self._validation_test()
                    print(text)

                case _:
                    print('Неизвестный вариант')
                    print(text)
