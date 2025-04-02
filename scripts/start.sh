#!/bin/sh

mkdir -p ~/bigbro_company_server

cd ~/bigbro_company_server

if [ ! -d ".git" ]; then
  git clone -b develop https://github.com/bigbroCO-team/bigbro_company_server .
else
  git pull origin develop
fi

docker build . -t bigbro-application

docker stop bigbro-application  || true

docker rm bigbro-application || true

docker run -d --name bigbro-application --env-file ~/.env bigbro-application