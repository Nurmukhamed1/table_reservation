#!/bin/bash

echo "✅ ENTRYPOINT SCRIPT STARTED"

echo "⏳ Waiting for DB to be ready..."
sleep 5  # минимальная задержка

echo "📦 Applying Alembic migrations..."
alembic upgrade head

echo "🚀 Starting FastAPI server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
