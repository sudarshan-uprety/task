#!/bin/bash

# Apply database migrations
#echo "Apply database migrations"

echo "Starting server"
python manage.py migrate
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:80 core.asgi -w 4 -k uvicorn.workers.UvicornWorker
