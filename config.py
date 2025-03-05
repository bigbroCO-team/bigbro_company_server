import os

from dotenv import load_dotenv

load_dotenv(f'.env.{os.environ.get('env')}')

SESSION_SECRET_KEY = os.environ.get('SESSION_SECRET_KEY')

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

KAKAO_API_KEY = os.environ.get('KAKAO_API_KEY')
KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI')
KAKAO_CLIENT_SECRET = os.environ.get('KAKAO_CLIENT_SECRET')