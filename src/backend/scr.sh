#!/bin/sh

if [ ! -d /app/src/backend/migrations ]; then
  alembic init /app/src/backend/migrations
fi

alembic -c /app/src/backend/alembic.ini revision --autogenerate -m "initial migration"

alembic -c /app/src/backend/alembic.ini upgrade head
python /app/src/backend/jwt_utils/crud.py
python /app/src/backend/books_utils/crud.py

# Запуск uvicorn
PYTHONPATH=${pwd} uvicorn main:app --host 0.0.0.0 --port 5000
