"""
Конфигурация приложения
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""

    # Основные настройки
    app_name: str = "Менеджер Задач"
    app_version: str = "1.0.0"
    debug: bool = False

    # Настройки базы данных
    database_url: str = "sqlite+aiosqlite:///./tasks.db"

    # Настройки для тестирования
    test_database_url: str = "sqlite+aiosqlite:///./test_tasks.db"

    model_config = SettingsConfigDict(env_file=".env")


# Глобальный экземпляр настроек
settings = Settings()
