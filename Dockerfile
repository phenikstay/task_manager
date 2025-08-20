# Простой Dockerfile для быстрой сборки
FROM python:3.12-slim

# Метаданные образа
LABEL maintainer="Task Manager API" \
      version="1.0.0" \
      description="Современный API для управления задачами на FastAPI"

# Создание пользователя для безопасности (не root)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY ./app ./app

# Создание директории для базы данных
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Переключение на пользователя appuser
USER appuser

# Настройка переменных окружения
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Открытие порта
EXPOSE 8000

# Health check для проверки состояния контейнера
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=10)" || exit 1

# Команда запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]