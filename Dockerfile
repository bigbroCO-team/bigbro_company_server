FROM python:3.13

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

RUN poetry run python src/manage.py migrate

CMD poetry run gunicorn --chdir ./src/ --bind 0.0.0.0:8000 --workers 3 core.wsgi:application