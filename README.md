# Лабораторная работа
Смирнов Вячеслав М8О-106БВ-25

# Модель задачи: дескрипторы и @property



## Структура проекта

 <pre>
    .
    ├── PythonTaskHandler                      # Кодовая база лабораторной работы
    │   ├── src/                               # Исходный код
    │   |   ├── core/                          # Основные абстракции и данные
    │   |   |   ├── __init__.py
    │   |   |   ├── cli.py                     # Описание класса CLI
    │   |   |   ├── constants.py               # Константы
    │   |   |   ├── contract.py                # Описание Protocol (TaskSource)
    │   |   |   ├── exceptions.py              # Кастомные исключения
    │   |   ├── logger/                        # Настройки логгера
    │   |   |   ├── setup_logger.py            # Создание логгера
    │   |   |   ├── config.py                  # Конфиг для логгера
    │   |   ├── models/                        # Модели
    │   |   |   ├── descriptors/               # Дескрипторы
    │   |   |   |   ├── __init__.py
    │   |   |   |   ├── base.py                # Базовый класс валидатора
    │   |   |   |   ├── numeric.py             # Числовые дескрипторы
    │   |   |   |   ├── text.py                # Текстовые дескрипторы
    │   |   |   |   ├── other.py               # Остальные дескрипторы
    │   |   |   ├── task.py                    # Описание модели задачи
    │   |   ├── sources/                       # Реализации источников
    │   |   |   ├── __init__.py
    │   |   |   ├── api_source.py              # Источник API-заглушка
    │   |   |   ├── file_source.py             # Источник файл
    │   |   |   ├── gen_source.py              # Генератор
    │   |   |   ├── input.json                 # Файл с задачами
    │   |   ├── __init__.py__
    │   |   ├── demonstration.py               # Функции для демонстрации
    │   |   ├── main.py                        # Точка входа
    │   |   ├── receiver.py                    # Модуль приёма задач и их валидации
    │   ├── tests/                             # Unit тесты
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
git clone https://github.com/yyeart/pythontaskhandler.git
cd PythonTaskHandler
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
* Программа покрыта юнит-тестами с использованием pytest и unittest.mock, процент покрытия >= 80%
* Запуск тестов: `pytest -v`
* Проверка покрытия тестов: `pytest -v --cov=src`

## Логирование
* Логи хранятся в файле shell.log и включают:
    * дату, время
    * номер шага, тип операции
    * сообщения об ошибках

## Допущения
* Файловым источником является заданный файл `input.json`
* Генератор задач задаёт `description` рандомно
* API-источник задач является заглушкой
