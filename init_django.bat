docker-compose exec -u root backend python manage.py makemigrations
docker-compose exec -u root backend python manage.py migrate
docker-compose exec -u root backend python create_fixtures.py
docker-compose exec -u root backend python manage.py createsuperuser