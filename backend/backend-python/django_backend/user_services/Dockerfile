# Image Python
FROM python:3.12.3-slim

# Working Directory
WORKDIR /jajancuy/django-sso

# Copy requirements.txt
COPY requirements.txt .

# Install library postgresql
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run
RUN python manage.py makemigrations
RUN python manage.py makemigrations acounts_managements
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# RUN GUNICORN
CMD ["gunicorn", "user_services.wsgi", "--bind", "0.0.0.0:5000"]