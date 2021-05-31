#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install -r requirements.txt
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver