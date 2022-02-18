sh reset_env.bat
docker network create --driver=bridge --subnet=192.168.0.0/16 bet-network
docker-compose build
docker-compose up -d .
sleep 10s
sh init_django.bat