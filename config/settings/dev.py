import os
from datetime import timedelta
from .base import *

DEBUG = True
ALLOWED_HOSTS = [ "localhost", "127.0.0.1" ]

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions"
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]

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

INTERNAL_IPS = [ "127.0.0.1" ]

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
        'level': 'DEBUG',
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
