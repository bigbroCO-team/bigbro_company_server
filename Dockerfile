FROM python:3.13

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

RUN poetry run python src/manage.py migrate

EXPOSE 80

CMD [ "poetry", "run", "gunicorn", "--chdir", "./src/",  "-b", "0.0.0.0:80", "core.wsgi:application" ]