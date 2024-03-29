# FastAPI project
Проект на FastAPI выполненный в качестве домашнего задания для МТС ШАД. Приложение представляет из себя электронную библиотеку, в которой есть книги и продавцы книг.

## Функционал проекта

- Добавление продавца
- Получение всех продавцов
- Получение одного продавца по ID
- Удаление/Изменение продавца

- Добавление книги
- Получение всех книг
- Получение одной книги по ID
- Удаление/Изменение книги

Также реализована Авторизация по JWT.


## Структура проекта

Для удобства и соблюдения принципов чистой архитектуры проект разделен на следующие пакеты:

- `configurations` — слой для хранения конфигураций, констант, параметров и настроек проекта.

- `models` — слой для хранения моделей (ORM или Data Classes).

- `routers` — слой для настроек URL для различных эндпоинтов.

- `schemas` — слой содержащий схемы pydantic, отвечает за сериализацию и валидацию.

- `tests` - слой содержащий тесты.

## Запуск приложения

```shell
make install_reqs

make up_compose

make run_app
```


## Used Libraries
- [FastAPI](https://fastapi.tiangolo.com)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Pytest](https://docs.pytest.org/en/8.0.x/)