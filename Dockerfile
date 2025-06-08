FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install uvicorn[standard]

COPY /brigantes .

# Collect static files
RUN python manage.py collectstatic --noinput --settings=brigantes.settings.prod

RUN DJANGO_SETTINGS_MODULE=brigantes.settings.prod gunicorn --bind 0.0.0.0:8000 brigantes.wsgi:application
