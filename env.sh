#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install django
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser (admin, admin@gmail.com, admin2020)