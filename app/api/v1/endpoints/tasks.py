"""
API endpoints для работы с задачами
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import task as task_crud
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskListResponse(BaseModel):
    """
    Схема ответа для списка задач с метаданными
    """

    tasks: List[TaskResponse]
    total: int
    skip: int
    limit: int


router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу",
    description="Создает новую задачу с указанными параметрами",
)
async def create_task(
    task_data: TaskCreate, db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Создание новой задачи
    """
    task = await task_crud.create_task(db=db, task_data=task_data)
    return TaskResponse.model_validate(task)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить задачу по ID",
    description="Возвращает задачу с указанным идентификатором",
)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)) -> TaskResponse:
    """
    Получение задачи по ID
    """
    task = await task_crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена",
        )
    return TaskResponse.model_validate(task)


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Получить список задач",
    description="Возвращает список задач с возможностью фильтрации и пагинации",
)
async def get_tasks(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(
        100, ge=1, le=1000, description="Максимальное количество возвращаемых записей"
    ),
    completed: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
    db: AsyncSession = Depends(get_db),
) -> TaskListResponse:
    """
    Получение списка задач с фильтрацией и пагинацией
    """
    tasks = await task_crud.get_tasks(
        db=db, skip=skip, limit=limit, completed=completed
    )
    total = await task_crud.get_tasks_count(db=db, completed=completed)

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновить задачу",
    description="Обновляет задачу с указанным идентификатором",
)
async def update_task(
    task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Обновление задачи
    """
    task = await task_crud.update_task(db=db, task_id=task_id, task_data=task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена",
        )
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет задачу с указанным идентификатором",
)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Удаление задачи
    """
    deleted = await task_crud.delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена",
        )
