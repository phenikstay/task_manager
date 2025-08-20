"""
Конфигурация базы данных
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""


# Создание движка базы данных
engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения сессии базы данных
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    """
    Создание всех таблиц в базе данных
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """
    Удаление всех таблиц из базы данных
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
