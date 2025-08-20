"""
Pydantic схемы для задач
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """
    Базовая схема задачи с общими полями
    """

    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    completed: bool = Field(False, description="Статус выполнения задачи")


class TaskCreate(TaskBase):
    """
    Схема для создания новой задачи
    """


class TaskUpdate(BaseModel):
    """
    Схема для обновления задачи
    """

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Название задачи"
    )
    description: Optional[str] = Field(None, description="Описание задачи")
    completed: Optional[bool] = Field(None, description="Статус выполнения задачи")


class TaskResponse(TaskBase):
    """
    Схема для ответа API с полной информацией о задаче
    """

    id: int = Field(..., description="Уникальный идентификатор задачи")
    created_at: datetime = Field(..., description="Дата и время создания задачи")
    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления задачи"
    )

    model_config = ConfigDict(from_attributes=True)
