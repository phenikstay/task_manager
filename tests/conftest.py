"""
Конфигурация тестов pytest
"""

import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

# Настройка движка для тестовой базы данных
test_engine = create_async_engine(settings.test_database_url, echo=False, future=True)

# Создание фабрики тестовых сессий
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Фикстура для создания event loop для всех тестов
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_test_db():
    """
    Фикстура для настройки тестовой базы данных
    """
    # Создание таблиц
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Очистка после тестов
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(setup_test_db) -> AsyncGenerator[AsyncSession, None]:
    """
    Фикстура для получения тестовой сессии базы данных
    """
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def test_client(db_session: AsyncSession):
    """
    Фикстура для получения тестового HTTP клиента
    """

    # Переопределение зависимости базы данных для тестов
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Очищаем переопределения
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    """
    Альтернативная фикстура для тестов в классах
    """

    # Переопределение зависимости базы данных для тестов
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Очищаем переопределения
    app.dependency_overrides.clear()


@pytest.fixture
def sample_task_data():
    """
    Фикстура с примерными данными задачи
    """
    return {
        "title": "Тестовая задача",
        "description": "Описание тестовой задачи",
        "completed": False,
    }


@pytest.fixture
async def created_task(test_client: AsyncClient, sample_task_data: dict):
    """
    Фикстура для создания тестовой задачи
    """
    response = await test_client.post("/api/v1/tasks/", json=sample_task_data)
    return response.json()
