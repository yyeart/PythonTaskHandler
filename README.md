# Лабораторная работа
Смирнов Вячеслав М8О-106БВ-25

# Источники задач и контракты



## Структура проекта

 <pre>
    .
    ├── python-lab-duck_typing                 # Кодовая база лабораторной работы
    │   ├── src/                               # Исходный код
    │   |   ├── core/                          # Основные абстракции и данные
    │   |   |   ├── __init__.py              
    │   |   |   ├── contract.py                # Описание Protocol (TaskSource)
    │   |   |   ├── models.py                  # Описание структуры Task
    │   |   ├── logger/                        # Настройка логгера
    │   |   |   ├── setup_logger.py            # Создание логгера
    │   |   |   ├── config.py                  # Конфиг для логгера
    │   |   ├── sources/                       # Реализации источников
    │   |   |   ├── __init__.py                
    │   |   |   ├── api_source.py              # Источник API-заглушка
    │   |   |   ├── file_source.py             # Источник файл
    │   |   |   ├── gen_source.py              # Генератор
    │   |   |   ├── input.json                 # Файл с задачами
    │   |   ├── __init__.py__
    │   |   ├── constants.py                   # Константы
    │   |   ├── main.py                        # Точка входа
    │   |   ├── receiver.py                    # Модуль приёма задач и их валидации
    │   ├── tests/                             # Unit тесты
    │   |   ├── __init__.py
    │   |   ├── conftest.py                    # Содержит фикстуры источников
    │   |   ├── test_api_source.py             # Тесты API-заглушки
    │   |   ├── test_core.py                   # Тесты основных структур
    │   |   ├── test_file_source.py            # Тесты файлового источника
    │   |   ├── test_generator_source.py       # Тесты генератора задач
    │   |   ├── test_receiver.py               # Тесты модуля приёма задач
    │   |   ├── test_repr.py                   # Тесты отображений
    │   ├── .gitignore                         # git ignore файл
    │   ├──.pre-commit-config.yaml             # Средства автоматизации проверки кодстайла
    │   ├── README.md                          # Описание проекта
    │   ├── pyproject.toml                     # Конфигурация проекта
    │   ├── requirements.txt                   # Зависимости
    │   ├── uv.lock                            # Зависимости
</pre>

## Установка и запуск
1. Склонируйте репозиторий:
```bash
git clone https://github.com/yyeart/python-lab-duck_typing.git
cd python-lab-duck_typing
```
2. Настройте окружение:
```bash
python -m venv .venv
source .venv/bin/activate # Для Linux/macOS
source .venv/scripts/activate # Для Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Запустите приложение:
```bash
python -m src.main
```

## Тестирование
* Все функции покрыты юнит-тестами с использованием pytest и unittest.mock, процент покрытия >= 80%
* Применяется `side_effect` для тестирования генератора случайных задач
* Запуск тестов: `pytest -v`
* Проверка покрытия тестов: `pytest -v --cov=src`

## Логирование
* Логи хранятся в файле shell.log и включают:
    * дату, время
    * номер шага, тип операции
    * сообщения об ошибках

## Допущения
* Под `payload` понимаются любые произвольные данные (тип `Any`)
* Файловым источником является заданный файл `input.json`
* Генератор задач задаёт `payload` рандомно
* API-источник задач является заглушкой
