import os
from datetime import timedelta
from .base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = False

# Database env values
DB_NAME = os.getenv("DB_NAME")
DB_USER_NM = os.getenv("DB_USER_NM")
DB_USER_PW = os.getenv("DB_USER_PW")
DB_IP = os.getenv("DB_IP")
DB_PORT = os.getenv("DB_PORT")

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER_NM,
        'PASSWORD': DB_USER_PW,
        'HOST': DB_IP,
        'PORT': DB_PORT,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}