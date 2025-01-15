import os

from .base import *


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}',
    }
}

KAKAO_CLIENT_REDIRECT_URL = 'https://bigbro.company/'
KAKAO_REDIRECT_URI = 'https://prod.api.bigbro.company/account/auth/kakao/callback'