sh stop_docker.bat
docker-compose up -d backend
docker-compose exec -u root backend sh -c "chown -R user:root /home/user/app"
docker-compose exec -u root backend sh -c "chown -R user:root /home/user/frontend/media"
docker-compose exec -u root backend sh -c "chown -R user:root /home/user/staticfiles"
docker-compose exec -u root backend sh -c "chown -R user:root /home/user/upload"
docker-compose exec -u root backend sh -c "chmod -R 777 /home/user/frontend/media"
docker-compose exec -u root backend sh -c "chmod -R 777 /home/user/staticfiles"
docker-compose exec -u root backend sh -c "chmod -R 777 /home/user/upload"
docker-compose exec -u root backend python manage.py collectstatic --noinput --clear
docker-compose exec -u root backend python manage.py makemigrations
docker-compose exec -u root backend python manage.py migrate
sh stop_docker.bat
sh start_docker.bat