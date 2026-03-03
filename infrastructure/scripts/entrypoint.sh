#!/bin/sh

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
alembic upgrade head

echo "Seeding database..."
python infrastructure/scripts/seed.py

echo "Starting API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
