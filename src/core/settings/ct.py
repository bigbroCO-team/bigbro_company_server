import os

from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-cache',
    }
}


KAKAO_CLIENT_REDIRECT_URL = '/'
KAKAO_REDIRECT_URI = '/account/auth/kakao/callback'