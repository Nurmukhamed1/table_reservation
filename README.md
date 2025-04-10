1. Создайте файл .env точно такой же как .env_example
2. docker compose up --build
3. При первом запуске автоматически применятся Alembic миграции и поднимется FastAPI сервер
4. Откройте http://localhost:8000/docs