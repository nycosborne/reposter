#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --processes 5 --master --enable-threads --module app.wsgi
#uwsgi --http :9000 --module app.wsgi:application --master --processes 5