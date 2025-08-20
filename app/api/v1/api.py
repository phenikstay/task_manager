"""
API роутер версии 1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import tasks

api_router = APIRouter()

# Подключение endpoints для задач
api_router.include_router(tasks.router, prefix="/tasks", tags=["Задачи"])
