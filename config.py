import os

from dotenv import load_dotenv

load_dotenv(f'.env.{os.environ.get('env')}')


DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
