#!/bin/sh


# ╨а╤Ы╨а┬╢╨а╤С╨а╥С╨а┬░╨а╨Е╨а╤С╨а┬╡ ╨а╥С╨а╤Х╨б╨Г╨бтАЪ╨б╤У╨а╤Ч╨а╨Е╨а╤Х╨б╨Г╨бтАЪ╨а╤С ╨а┬▒╨а┬░╨а┬╖╨бтА╣ ╨а╥С╨а┬░╨а╨Е╨а╨Е╨бтА╣╨бтАж
python manage.py shell -c "from django.db import connections; from django.db.utils import OperationalError; import time; db_conn = None; while not db_conn:;     try:;         db_conn = connections[\"default\"];     except OperationalError:;         print(\"Database unavailable, waiting 1 second...\");         time.sleep(1);"

# ╨а╤Я╨б╨В╨а╤С╨а╤Ш╨а┬╡╨а╨Е╨а┬╡╨а╨Е╨а╤С╨а┬╡ ╨а╤Ш╨а╤С╨а╤Ц╨б╨В╨а┬░╨бтАа╨а╤С╨атДЦ ╨а┬▒╨а┬░╨а┬╖╨бтА╣ ╨а╥С╨а┬░╨а╨Е╨а╨Е╨бтА╣╨бтАж
echo "Applying database migrations..."
python manage.py migrate

# ╨а╨О╨а┬▒╨а╤Х╨б╨В ╨б╨Г╨бтАЪ╨а┬░╨бтАЪ╨а╤С╨бтАб╨а┬╡╨б╨Г╨а╤Ф╨а╤С╨бтАж ╨бтАЮ╨а┬░╨атДЦ╨а┬╗╨а╤Х╨а╨Ж
echo "Collecting static files..."
python manage.py collectstatic --noinput

# ╨а╨О╨а╤Х╨а┬╖╨а╥С╨а┬░╨а╨Е╨а╤С╨а┬╡ ╨б╨Г╨б╤У╨а╤Ч╨а┬╡╨б╨В╨а╤Ч╨а╤Х╨а┬╗╨б╨К╨а┬╖╨а╤Х╨а╨Ж╨а┬░╨бтАЪ╨а┬╡╨а┬╗╨б╨П, ╨а┬╡╨б╨Г╨а┬╗╨а╤С ╨а╤Х╨а╨Е ╨а╨Е╨а┬╡ ╨б╨Г╨б╤У╨бтА░╨а┬╡╨б╨Г╨бтАЪ╨а╨Ж╨б╤У╨а┬╡╨бтАЪ
echo "Creating superuser if it does not exist..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# ╨атАФ╨а┬░╨а╤Ч╨б╤У╨б╨Г╨а╤Ф Gunicorn
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
