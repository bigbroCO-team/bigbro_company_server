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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}',
    }
}

KAKAO_CLIENT_REDIRECT_URL = 'https://stage.bigbro.company/main'
KAKAO_REDIRECT_URI = 'http://ec2-3-39-233-10.ap-northeast-2.compute.amazonaws.com:8000/account/auth/kakao/callback'


import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)