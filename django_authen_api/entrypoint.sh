#!/bin/sh

python manage.py migrate 
gunicorn django_authen_api.wsgi:application --bind 0.0.0.0:$PORT