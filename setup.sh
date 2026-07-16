#!/usr/bin/env bash
set -e

echo "VineMind AI — Development Setup"
echo "================================"

if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env created from .env.example"
fi

echo "Starting services..."
docker compose up -d postgres

echo "Waiting for PostgreSQL..."
sleep 3

echo "Running database setup and seeding..."
cd backend
python -m seed

echo ""
echo "VineMind AI is ready!"
echo "  Backend API:  http://localhost:8000"
echo "  API Docs:     http://localhost:8000/docs"
echo "  Database:     localhost:5432"
echo ""
echo "Demo login: jeffrey@vinemind.ai / demo1234"
