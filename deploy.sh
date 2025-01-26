#!/bin/sh

IS_BLUE=$(docker ps | grep blue)

if [ -z "$IS_BLUE" ]; then
    echo "Deploying blue"

    docker-compose -f infra/compose/docker-compose.yml up --build -d web-blue
    docker-compose -f infra/compose/docker-compose.yml down web-green
else
    echo "Deploying green"
    docker-compose -f infra/compose/docker-compose.yml up --build -d web-green
    docker-compose -f infra/compose/docker-compose.yml down web-blue
fi
