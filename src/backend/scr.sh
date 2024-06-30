#!/bin/sh

if [ ! -d /app/src/backend/migrations ]; then
  alembic init /app/src/backend/migrations
fi
sleep 5
alembic revision --autogenerate -m "initial migration"

alembic upgrade head
python jwt_utils/crud.py
python books_utils/crud.py

# Запуск uvicorn
PYTHONPATH=${pwd} uvicorn main:app --host 0.0.0.0 --port 5000
