import os
from datetime import timedelta
from .base import *

BOT_MODE = "polling"


if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
        "query_counter",
    ]

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "query_counter.middleware.DjangoQueryCounterMiddleware",
    ]

    INTERNAL_IPS = ["127.0.0.1"]

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
        "ROTATE_REFRESH_TOKENS": True,
        "BLACKLIST_AFTER_ROTATION": True,
        "AUTH_HEADER_TYPES": ("Bearer",),
    }

    CORS_ALLOW_ALL_ORIGINS = True
