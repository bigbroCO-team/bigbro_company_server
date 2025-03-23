#!/bin/sh

mkdir -p ~/bigbro_company_server

cd ~/bigbro_company_server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/bigbroCO-team/bigbro_company_server .
else
  git pull origin develop
fi

docker-compsose up --build -d

docker container prune -f
docker image prune -a -f
