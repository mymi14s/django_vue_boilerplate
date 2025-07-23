FROM python:3.11-slim AS builder

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
COPY requirements.txt /opt/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install uvicorn[standard]

# Copy application code
COPY brigantes /opt

# Collect static files
RUN python manage.py collectstatic --noinput --settings=brigantes.settings.prod

# Production stage
FROM python:3.11-slim

WORKDIR /opt

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies - this is the key fix
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /opt /opt

# Copy static files
COPY --from=builder /opt/static /opt/static

# Configure Nginx
COPY nginx.conf /etc/nginx/nginx.conf
RUN rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
RUN nginx -t

# Make scripts executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

