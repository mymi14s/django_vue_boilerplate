#!/bin/bash
set -e

# Create log directory
mkdir -p /var/log
python3.11 -m venv env11
source env11/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput --settings=brigantes.settings.prod

# Start Django in background
echo "Starting Django application..."
python -m uvicorn brigantes.asgi:application --host 127.0.0.1 --port 8000 --workers 4 &
DJANGO_PID=$!

# Start Nginx in foreground
echo "Starting Nginx..."
nginx -g "daemon off;"