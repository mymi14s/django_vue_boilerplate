FROM python:3.11-slim

WORKDIR /opt

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install uvicorn[standard]

# Copy application code
COPY brigantes /opt


# Start the server using uvicorn
# CMD [ "python", "manage.py",  "migrate", "--settings=brigantes.settings.prod", \

# CMD ["uvicorn", "brigantes.asgi:application", "--reload", "--host", "0.0.0.0"]
 
# Collect static files
# RUN python manage.py collectstatic --noinput --settings=brigantes.settings.prod

# RUN DJANGO_SETTINGS_MODULE=brigantes.settings.prod gunicorn --bind 0.0.0.0:8000 brigantes.wsgi:application
# RUN uvicorn brigantes.asgi:application --reload


# DJANGO_SECRET_KEY='sdftghjk'
# DJANGO_SETTINGS_MODULE=brigantes.settings.prod
# DJANGO_DATABASE_URL=mysql://root:root@0.0.0.0:3306/brigantes

# docker run -d \
#   --name brigantes_app \
#   --network host \
#   -e DJANGO_SECRET_KEY=efsdgewdgf \
#   -e DJANGO_SETTINGS_MODULE=brigantes.settings.prod \
#   -e DJANGO_DATABASE_URL=mysql://root:root@host.docker.internal:3306/brigantes \
#   brigantes python manage.py migrate --noinput --settings=brigantes.settings.prod

# docker run -d \
#   --name brigantes_app \
#   --network host \
#   -p 8000:8000 \
#   -e DJANGO_SECRET_KEY=efsdgewdgf \
#   -e DJANGO_SETTINGS_MODULE=brigantes.settings.prod \
#   -e DJANGO_DATABASE_URL=mysql://root:root@host.docker.internal:3306/brigantes \
#   brigantes python manage.py migrate --noinput --settings=brigantes.settings.prod