# Менеджер Задач

Современное API для управления задачами, построенное на FastAPI с использованием лучших практик разработки.

## Возможности

- ✅ **Полный CRUD функционал** - создание, получение, обновление и удаление задач
- 🔍 **Фильтрация и поиск** - поиск задач по статусу выполнения
- 📄 **Пагинация** - разбиение больших списков на страницы
- 🚀 **Асинхронная архитектура** - высокая производительность благодаря async/await
- 📊 **Автоматическая документация** - Swagger UI и ReDoc
- 🧪 **Полное покрытие тестами** - надежность и качество кода
- 🐍 **Современный Python** - использование Python 3.12+ и SQLAlchemy 2.0
- 🗄️ **SQLite база данных** - простота развертывания и использования

## Технологии

- **FastAPI** - современный веб-фреймворк для создания API
- **SQLAlchemy 2.0** - асинхронная ORM для работы с базой данных
- **Pydantic** - валидация данных и сериализация
- **SQLite** - легковесная база данных
- **pytest** - фреймворк для тестирования
- **asyncio** - асинхронное программирование

## Быстрый старт

### Способ 1: Запуск с Docker (рекомендуется)

```bash
# Клонирование репозитория
git clone <repository_url>
cd task_manager

# Запуск с Docker Compose
docker compose up --build

# Запуск в фоновом режиме
docker compose up -d --build
```

### Способ 2: Локальная установка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Доступ к API

**При локальном запуске:**
- **API**: http://localhost:8000/api/v1/tasks
- **Документация (Swagger)**: http://localhost:8000/docs
- **Альтернативная документация (ReDoc)**: http://localhost:8000/redoc

**При запуске с Docker:**
- **API**: http://localhost:8080/api/v1/tasks
- **Документация (Swagger)**: http://localhost:8080/docs
- **Альтернативная документация (ReDoc)**: http://localhost:8080/redoc

## API Endpoints

### Задачи

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/v1/tasks/` | Создание новой задачи |
| `GET` | `/api/v1/tasks/{id}` | Получение задачи по ID |
| `GET` | `/api/v1/tasks/` | Получение списка задач |
| `PUT` | `/api/v1/tasks/{id}` | Обновление задачи |
| `DELETE` | `/api/v1/tasks/{id}` | Удаление задачи |

### Параметры запросов

#### GET /api/v1/tasks/
- `skip` (int) - количество пропускаемых записей (по умолчанию: 0)
- `limit` (int) - максимальное количество записей (по умолчанию: 100, максимум: 1000)
- `completed` (bool) - фильтр по статусу выполнения (опционально)

## Примеры использования

### Создание задачи

**Локальный запуск:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Изучить FastAPI",
       "description": "Пройти документацию и создать тестовый проект",
       "completed": false
     }'
```

**Docker запуск:**
```bash
curl -X POST "http://localhost:8080/api/v1/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Изучить FastAPI",
       "description": "Пройти документацию и создать тестовый проект",
       "completed": false
     }'
```

### Получение списка задач

**Локальный запуск:**
```bash
curl "http://localhost:8000/api/v1/tasks/?limit=10&completed=false"
```

**Docker запуск:**
```bash
curl "http://localhost:8080/api/v1/tasks/?limit=10&completed=false"
```

### Обновление задачи

**Локальный запуск:**
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

**Docker запуск:**
```bash
curl -X PUT "http://localhost:8080/api/v1/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

## Тестирование

### Запуск всех тестов

```bash
pytest
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск конкретного теста

```bash
pytest tests/test_api_simple.py::test_create_and_get_task -v
```

### Покрытие тестами

```bash
pytest --cov=app
```

## Структура проекта

```
app/
├── __init__.py
├── main.py                 # Главный файл приложения
├── core/
│   ├── __init__.py
│   ├── config.py          # Конфигурация приложения
│   └── database.py        # Настройка базы данных
├── models/
│   ├── __init__.py
│   └── task.py            # SQLAlchemy модели
├── schemas/
│   ├── __init__.py
│   └── task.py            # Pydantic схемы
├── crud/
│   ├── __init__.py
│   └── task.py            # CRUD операции
└── api/
    ├── __init__.py
    └── v1/
        ├── __init__.py
        ├── api.py         # Главный роутер API
        └── endpoints/
            ├── __init__.py
            └── tasks.py   # Endpoints для задач

tests/
├── __init__.py
├── conftest.py            # Фикстуры для тестов
├── test_basic.py          # Базовые тесты (health, root)
└── test_api_simple.py     # API тесты (CRUD операции)
```

## Особенности реализации

### Асинхронная архитектура
Приложение полностью построено на асинхронной архитектуре:
- Асинхронные базы данных (aiosqlite)
- Асинхронные CRUD операции
- Асинхронные API endpoints

### Валидация данных
Использование Pydantic обеспечивает:
- Автоматическую валидацию входящих данных
- Сериализацию ответов API
- Автогенерацию OpenAPI схемы

### Обработка ошибок
- Корректная обработка ошибок 404 для несуществующих ресурсов
- Валидация данных с возвратом ошибки 422
- Информативные сообщения об ошибках на русском языке

### Качество кода
- Соблюдение PEP8
- Типизация с использованием Type Hints
- Комментарии и документация на русском языке
- Полное покрытие тестами

## Разработка

### Локальная разработка

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Запустите приложение: `uvicorn app.main:app --reload`
4. Откройте http://localhost:8000/docs для работы с API (или http://localhost:8080/docs при Docker)

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=app --cov-report=html

# Только быстрые тесты
pytest -m "not slow"
```

## Docker

### 🐳 Запуск с Docker

#### Быстрый запуск
```bash
# Сборка и запуск
docker compose up --build

# Запуск в фоновом режиме
docker compose up -d --build

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down
```

#### Режимы запуска

**Продакшн (по умолчанию):**
```bash
docker compose up --build
# Доступ: http://localhost:8080
```

**Разработка с hot-reload:**
```bash
docker compose --profile dev up --build
# Доступ: http://localhost:8001
```

**Продакшн с Nginx:**
```bash
docker compose --profile production up --build
# Доступ: http://localhost:80
```

#### Работа с контейнерами

```bash
# Выполнение команд в контейнере
docker compose exec task-manager bash

# Запуск тестов в контейнере
docker compose exec task-manager pytest

# Просмотр логов
docker compose logs task-manager

# Пересборка образа
docker compose build --no-cache
```

#### Управление данными

```bash
# Просмотр volumes
docker volume ls

# Удаление данных (ОСТОРОЖНО!)
docker compose down -v

# Backup базы данных
docker cp task-manager-api:/app/data/tasks.db ./backup-tasks.db
```

### 🔧 Dockerfile особенности

- **Оптимизированный single-stage build** для простоты
- **Non-root пользователь** для безопасности  
- **Health checks** для мониторинга
- **Правильные переменные окружения**
- **Оптимизированные слои** для быстрой сборки

## Технические решения

### Почему FastAPI?
- Высокая производительность
- Автоматическая генерация документации
- Современный Python с поддержкой async/await
- Встроенная валидация данных через Pydantic

### Почему SQLAlchemy 2.0?
- Современный асинхронный API
- Типизированные запросы
- Отличная поддержка миграций
- Высокая производительность

### Почему SQLite?
- Простота развертывания
- Отсутствие внешних зависимостей
- Отличная производительность для небольших и средних приложений
- Легкость тестирования

### Почему Docker?
- Консистентная среда выполнения
- Простое развертывание
- Изоляция зависимостей
- Масштабируемость