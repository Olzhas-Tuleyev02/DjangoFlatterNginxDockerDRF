#!/bin/sh

# Ожидание доступности базы данных
# python manage.py shell -c "from django.db import connections; from django.db.utils import OperationalError; import time; db_conn = None; while not db_conn:;     try:;         db_conn = connections[\"default\"];     except OperationalError:;         print(\"Database unavailable, waiting 1 second...\");         time.sleep(1);" 

# Применение миграций базы данных
# echo "Applying database migrations..."
# python manage.py migrate

# Сбор статических файлов
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Создание суперпользователя, если он не существует
# echo "Creating superuser if it does not exist..."
# python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# Запуск Gunicorn
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
