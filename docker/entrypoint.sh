#!/bin/sh

set -e

# init nginx
if [ ! -d /run/nginx ]; then
    mkdir -p /run/nginx
    chown -R nginx.nginx /run/nginx
fi

# init blog
if [ ! -f /blog/db.sqlite3 ]; then
    python manage.py collectstatic
    python manage.py makemigrations
    python manage.py migrate
fi

nginx
gunicorn --workers=2 --bind=0.0.0.0:8000 my_blog.wsgi:application
