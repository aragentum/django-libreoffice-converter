#!/bin/sh

set -e

until python manage.py migrate; do
  echo "Migration problems, possibly DB server is unavailable"
  sleep 5
done

python manage.py collectstatic --no-input --clear
gunicorn -c gunicorn.py --log-config logging.conf web.wsgi
