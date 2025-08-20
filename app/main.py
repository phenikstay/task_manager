"""
Главный файл FastAPI приложения "Менеджер Задач"
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Обработчик жизненного цикла приложения
    """
    # Создание таблиц в базе данных при запуске
    await create_tables()
    yield


# Создание FastAPI приложения
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## API для управления задачами

    Этот API предоставляет возможности для полного управления задачами:

    * **Создание задач** - добавление новых задач с названием и описанием
    * **Просмотр задач** - получение задач по ID или списка всех задач
    * **Обновление задач** - изменение названия, описания или статуса выполнения
    * **Удаление задач** - удаление ненужных задач
    * **Фильтрация задач** - поиск задач по статусу выполнения
    * **Пагинация** - разбиение больших списков на страницы

    ### Основные возможности:
    - Асинхронная работа с базой данных
    - Валидация данных через Pydantic
    - Автоматическая документация API
    - Поддержка фильтрации и сортировки
    """,
    openapi_tags=[
        {
            "name": "Задачи",
            "description": (
                "Операции с задачами: создание, получение, " "обновление и удаление."
            ),
        }
    ],
    lifespan=lifespan,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение API роутеров
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Информация"])
async def read_root():
    """
    Корневой endpoint с информацией о приложении
    """
    return {
        "message": f"Добро пожаловать в {settings.app_name}!",
        "version": settings.app_version,
        "docs_url": "/docs",
        "api_prefix": "/api/v1",
    }


@app.get("/health", tags=["Информация"])
async def health_check():
    """
    Проверка состояния приложения
    """
    return {"status": "OK", "message": "Приложение работает корректно"}
