#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py fill_locations
python manage.py transport_add
