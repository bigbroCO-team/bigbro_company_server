#!/bin/sh

cd ~/bigbro_company_server

docker build -t bigbro .

docker stop bigbro || true

docker rm bigbro || true

docker run -d -p 80:80 --name bigbro --env-file ~/.env bigbro