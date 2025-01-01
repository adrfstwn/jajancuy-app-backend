# Base image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /jajancuy/django-sso

# Copy requirements.txt
COPY requirements.txt .

# Set DEBIAN_FRONTEND to noninteractive to avoid terminal-based configuration prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install PostgreSQL dependencies and gcc
RUN apt-get update && \
    apt-get install -y gcc libpq-dev apt-utils && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run migrations, collectstatic in a single RUN command to reduce layers
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 5000

# Menambahkan perintah collectstatic dalam Dockerfile
RUN python manage.py collectstatic --noinput

# Start Gunicorn
CMD ["gunicorn", "user_services.wsgi", "--bind", "0.0.0.0:5000"]
