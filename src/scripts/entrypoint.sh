#!/bin/sh
set -e

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Configuring bot webhook..."
python manage.py botwebhook set

echo "Starting server..."
python -m uvicorn config.server.asgi:application --host 0.0.0.0 --port 8000 --workers 4 --lifespan off
