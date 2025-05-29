#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z "$DB_HOST" 5432; do
  sleep 1
done

echo "PostgreSQL is working!"

python manage.py migrate
exec "$@"
