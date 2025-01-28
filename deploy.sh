#!/bin/sh

IS_BLUE=$(docker ps | grep blue)

# Blue-green 배포
if [ -z "$IS_BLUE" ]; then
    echo "Deploying blue"

    docker-compose -f infra/compose/docker-compose.yml up --build -d web-blue
    docker-compose -f infra/compose/docker-compose.yml down web-green
else
    echo "Deploying green"
    docker-compose -f infra/compose/docker-compose.yml up --build -d web-green
    docker-compose -f infra/compose/docker-compose.yml down web-blue
fi

# Health check
if curl http://localhost:80/health-check | grep 502; then
    echo "Health check failed"
    
    # Rollback
    if [ -z "$IS_BLUE" ]; then
        echo "Rolling back to blue"

        docker-compose -f infra/compose/docker-compose.yml up -d web-green
        docker-compose -f infra/compose/docker-compose.yml down web-blue
        docker system prune -af --volumes=false
        exit 1
    else
        echo "Rolling back to green"

        docker-compose -f infra/compose/docker-compose.yml up -d web-blue
        docker-compose -f infra/compose/docker-compose.yml down web-green
        docker system prune -af --volumes=false
        exit 1
    fi
else
    echo "Health check passed"
    docker system prune -af --volumes=false
fi