#!/bin/sh

mkdir -p ~/bigbro_company_server

cd ~/bigbro_company_server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/bigbroCO-team/bigbro_company_server .
else
  git pull origin develop
fi

docker build -t bigbro .

docker stop bigbro || true

docker rm bigbro || true

docker run -d -p 80:80 --name bigbro --env-file ~/.env bigbro

docker exec bigbro poetry run python /app/src/manage.py migrate