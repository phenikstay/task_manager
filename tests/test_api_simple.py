"""
Простые тесты API без сложных фикстур
"""

import pytest
from httpx import AsyncClient

from app.core.database import create_tables
from app.main import app


@pytest.mark.asyncio
async def test_create_and_get_task():
    """Тест создания и получения задачи"""
    # Создаем таблицы в базе данных
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем задачу
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "completed": False,
        }

        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201

        created_task_data = create_response.json()
        assert created_task_data["title"] == task_data["title"]
        assert created_task_data["description"] == task_data["description"]
        assert created_task_data["completed"] == task_data["completed"]
        assert "id" in created_task_data

        # Получаем созданную задачу
        task_id = created_task_data["id"]
        get_response = await client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 200

        retrieved_task = get_response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == task_data["title"]


@pytest.mark.asyncio
async def test_get_tasks_list():
    """Тест получения списка задач"""
    # Создаем таблицы в базе данных
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Получаем список задач
        response = await client.get("/api/v1/tasks/")
        assert response.status_code == 200

        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        assert isinstance(data["tasks"], list)


@pytest.mark.asyncio
async def test_update_task():
    """Тест обновления задачи"""
    # Создаем таблицы в базе данных
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем задачу
        task_data = {"title": "Задача для обновления"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Обновляем задачу
        update_data = {"completed": True}
        update_response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        assert update_response.status_code == 200

        updated_task = update_response.json()
        assert updated_task["completed"] is True
        assert updated_task["title"] == task_data["title"]  # Не изменилось


@pytest.mark.asyncio
async def test_delete_task():
    """Тест удаления задачи"""
    # Создаем таблицы в базе данных
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем задачу
        task_data = {"title": "Задача для удаления"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Удаляем задачу
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}")
        assert delete_response.status_code == 204

        # Проверяем, что задача удалена
        get_response = await client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_task_validation():
    """Тест валидации данных задачи"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Тест с пустым названием
        task_data = {"title": ""}
        response = await client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422

        # Тест со слишком длинным названием
        task_data = {"title": "x" * 201}
        response = await client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_not_found_errors():
    """Тест ошибок 404"""
    # Создаем таблицы в базе данных
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Получение несуществующей задачи
        response = await client.get("/api/v1/tasks/999999")
        assert response.status_code == 404

        # Обновление несуществующей задачи
        response = await client.put("/api/v1/tasks/999999", json={"title": "test"})
        assert response.status_code == 404

        # Удаление несуществующей задачи
        response = await client.delete("/api/v1/tasks/999999")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_tasks_filtering():
    """Тест фильтрации задач по completed статусу"""
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем задачи с разным статусом
        await client.post("/api/v1/tasks/", json={"title": "Завершенная", "completed": True})
        await client.post("/api/v1/tasks/", json={"title": "Незавершенная", "completed": False})

        # Получаем только завершенные
        response = await client.get("/api/v1/tasks/?completed=true")
        assert response.status_code == 200
        data = response.json()
        assert all(task["completed"] for task in data["tasks"])

        # Получаем только незавершенные
        response = await client.get("/api/v1/tasks/?completed=false")
        assert response.status_code == 200
        data = response.json()
        assert all(not task["completed"] for task in data["tasks"])


@pytest.mark.asyncio
async def test_pagination_parameters():
    """Тест пагинации"""
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем несколько задач
        for i in range(3):
            await client.post("/api/v1/tasks/", json={"title": f"Задача {i}"})

        # Тест пагинации
        response = await client.get("/api/v1/tasks/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 0
        assert data["limit"] == 2
        assert len(data["tasks"]) <= 2


@pytest.mark.asyncio
async def test_update_with_empty_data():
    """Тест обновления задачи пустыми данными"""
    await create_tables()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем задачу
        response = await client.post("/api/v1/tasks/", json={"title": "Исходная задача"})
        task_id = response.json()["id"]
        original_title = response.json()["title"]

        # Обновляем пустыми данными
        response = await client.put(f"/api/v1/tasks/{task_id}", json={})
        assert response.status_code == 200
        assert response.json()["title"] == original_title  # Не изменилось
