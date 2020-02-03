#!/bin/sh

set -e

until python manage.py migrate; do
  echo "Migration problems, possibly DB server is unavailable"
  sleep 5
done

gunicorn -c gunicorn.py --log-config logging.conf web.wsgi
