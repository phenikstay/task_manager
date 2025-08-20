"""
CRUD операции для работы с задачами
"""

from typing import List, Optional

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, task_data: TaskCreate) -> Task:
    """
    Создание новой задачи

    Args:
        db: Сессия базы данных
        task_data: Данные для создания задачи

    Returns:
        Созданная задача
    """
    task = Task(**task_data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(db: AsyncSession, task_id: int) -> Optional[Task]:
    """
    Получение задачи по ID

    Args:
        db: Сессия базы данных
        task_id: ID задачи

    Returns:
        Задача или None, если не найдена
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def get_tasks(
    db: AsyncSession, skip: int = 0, limit: int = 100, completed: Optional[bool] = None
) -> List[Task]:
    """
    Получение списка задач с фильтрацией и пагинацией

    Args:
        db: Сессия базы данных
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей
        completed: Фильтр по статусу выполнения (None - все задачи)

    Returns:
        Список задач
    """
    query = select(Task)

    if completed is not None:
        query = query.where(Task.completed == completed)

    query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_task(
    db: AsyncSession, task_id: int, task_data: TaskUpdate
) -> Optional[Task]:
    """
    Обновление задачи

    Args:
        db: Сессия базы данных
        task_id: ID задачи
        task_data: Данные для обновления

    Returns:
        Обновленная задача или None, если не найдена
    """
    # Получаем существующую задачу
    task = await get_task(db, task_id)
    if not task:
        return None

    # Обновляем только переданные поля
    update_data = task_data.model_dump(exclude_unset=True)
    if not update_data:
        return task

    # Выполняем обновление
    await db.execute(update(Task).where(Task.id == task_id).values(**update_data))
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """
    Удаление задачи

    Args:
        db: Сессия базы данных
        task_id: ID задачи

    Returns:
        True, если задача была удалена, False - если не найдена
    """
    # Проверяем существование задачи
    task = await get_task(db, task_id)
    if not task:
        return False

    # Удаляем задачу
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
    return True


async def get_tasks_count(db: AsyncSession, completed: Optional[bool] = None) -> int:
    """
    Получение общего количества задач

    Args:
        db: Сессия базы данных
        completed: Фильтр по статусу выполнения (None - все задачи)

    Returns:
        Количество задач
    """
    query = select(func.count(Task.id))  # pylint: disable=not-callable

    if completed is not None:
        query = query.where(Task.completed == completed)

    result = await db.execute(query)
    count = result.scalar()
    return count if count is not None else 0
