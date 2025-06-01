FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

EXPOSE 80

RUN chmod +x ./docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
