#!/bin/bash
virtualenv .env -p python3
. .env/bin/activate && pip install -r requirements.txt
. .env/bin/activate && python manage.py makemigrations
. .env/bin/activate && python manage.py migrate
# python manage.py runserver