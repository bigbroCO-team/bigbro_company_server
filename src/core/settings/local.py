import os

from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME", "bigbro"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASS", "postgres"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

KAKAO_CLIENT_REDIRECT_URL = "http://127.0.0.1:8000/"
KAKAO_REDIRECT_URI = "http://127.0.0.1:8000/account/auth/kakao/callback"
