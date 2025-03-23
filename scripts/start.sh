#!/bin/sh

cd  ~/bigbro_company_server/src/
poetry install
poetry run gunicorn --chdir ~/bigbro_company_server/src/ --bind 0.0.0.0:8000 --workers 3 core.wsgi:application