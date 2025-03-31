FROM python:3.13

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

EXPOSE 8000

CMD [
    "poetry", "run", "gunicorn",
    "--chdir", "./src/",
    "-b", "0.0.0.0:8000",
    "core.wsgi:application",
    "--access-logfile", "-",
    "--error-logfile", "-",
    "--log-level", "info"
]