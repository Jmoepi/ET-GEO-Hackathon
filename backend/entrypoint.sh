#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Seeding demo data..."
python seed.py || echo "Seed skipped (data may already exist)"

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
