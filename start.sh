#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Checking if superuser exists..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', 'admin')" \
| python manage.py shell

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
