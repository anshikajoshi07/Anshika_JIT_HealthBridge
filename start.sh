#!/bin/sh
set -e

: "${PORT:=8000}"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn on port $PORT"
exec gunicorn healthcare.wsgi:application --bind "0.0.0.0:$PORT" --workers 4 --worker-class sync --timeout 60

