#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PSQL_HOST $PSQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py fill_locations
python manage.py transport_add
python manage.py runserver 0.0.0.0:8000

exec "$@"