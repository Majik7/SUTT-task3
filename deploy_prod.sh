#!/bin/bash
set -e

echo "Giving permission to entrypoint"
chmod +x entrypoint.prod.sh

echo "Starting deployment"
docker compose -f docker-compose.prod.yml down

echo "Building and starting containers"
docker compose -f docker-compose.prod.yml up --build -d

echo "Running migrations"
docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

echo "Collecting static files"
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear

echo "Populating Database"
docker compose -f docker-compose.prod.yml exec web python manage.py populate

echo "Cleaning up old images"
docker image prune -f

echo "Deployment complete"
docker compose -f docker-compose.prod.yml logs -f web