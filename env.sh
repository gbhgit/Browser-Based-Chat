#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install django
. .env/bin/activate && pip install djangorestframework
. .env/bin/activate && pip install channels
. .env/bin/activate && pip install channels_redis
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser (admin, admin@gmail.com, admin2020)