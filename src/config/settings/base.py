from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = config("DEBUG", default=False, cast=bool)
SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure-change-me")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
DATABASE_URL = f"postgres://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}/{config('POSTGRES_DB')}"

UNFOLD_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    # 'unfold.contrib.constance',
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

LOCAL_APPS = [
    "account",
    "core",
    "api",
    "bot",
]

INSTALLED_APPS = UNFOLD_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "config.server.asgi.application"
WSGI_APPLICATION = "config.server.wsgi.application"

DATABASES = {
    "default": dj_database_url.parse(
        url=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locales"]

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATIC_ROOT = BASE_DIR.parent / "cdn/static"
MEDIA_ROOT = BASE_DIR.parent / "cdn/media"

# Logging
LOGGING_TELEGRAM_BOT_TOKEN = config("LOGGING_TELEGRAM_BOT_TOKEN", default="")
LOGGING_TELEGRAM_CHAT_ID = config("LOGGING_TELEGRAM_CHAT_ID", default="")

# Telegram Bot
BOT_TOKEN = config("BOT_TOKEN", default="")
BOT_MODE = config("BOT_MODE", default="polling")
BOT_WEBHOOK_BASE_URL = config("BOT_WEBHOOK_BASE_URL", default="")
BOT_WEBHOOK_PATH = config("BOT_WEBHOOK_PATH", default="/bot/webhook/")
BOT_WEBHOOK_SECRET = config("BOT_WEBHOOK_SECRET", default="")
BOT_PARSE_MODE = config("BOT_PARSE_MODE", default="HTML")
BOT_DEFAULT_LOCALE = config("BOT_DEFAULT_LOCALE", default="en")
BOT_FALLBACK_LOCALE = config("BOT_FALLBACK_LOCALE", default="en")

# Ensure logs directory exists
os.makedirs(BASE_DIR.parent / "logs", exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_context": {
            "()": "core.utils.logging.RequestContextFilter",
        },
    },
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "%(log_color)s[%(asctime)s] [%(levelname)s] "
                "%(name)s:%(module)s:%(filename)s:%(lineno)d "
                "%(funcName)s | %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "verbose": {
            "format": (
                "[%(asctime)s] [%(levelname)s] "
                "%(name)s:%(module)s:%(filename)s:%(lineno)d "
                "%(funcName)s | %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "telegram": {
            "format": (
                "*🚨 Django Error Alert (500)*\n"
                "*Level:* %(levelname)s\n"
                "*Message:* %(message)s\n\n"
                "*Module:* `%(module)s:%(filename)s:%(lineno)d`\n"
                "*Function:* `%(funcName)s`\n\n"
                "*User:* %(user)s\n"
                "*Method:* %(method)s\n"
                "*Path:* %(path)s\n"
                "*IP:* %(ip)s\n\n"
                "*Traceback:*\n```\n%(traceback)s\n```"
            )
        },
    },
    "handlers": {
        # Console
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        # Main app log (rotating)
        "app_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "../logs/app.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
        # Error log (rotating)
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "../logs/error.log",
            "when": "midnight",
            "backupCount": 60,
            "formatter": "verbose",
        },
        # Slow queries
        "slow_queries_file": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "../logs/slow_queries.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
        },
        # Telegram alerts
        "telegram_errors": {
            "level": "ERROR",
            "class": "core.utils.logging.TelegramErrorHandler",
            "bot_token": LOGGING_TELEGRAM_BOT_TOKEN,
            "chat_id": LOGGING_TELEGRAM_CHAT_ID,
            "filters": ["request_context"],
            "formatter": "telegram",
        },
    },
    "loggers": {
        # Django internal logs
        "django": {
            "handlers": ["app_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        # Django request errors → TELEGRAM!
        "django.request": {
            "handlers": ["telegram_errors", "error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        # Slow queries
        "django.db.backends": {
            "handlers": ["slow_queries_file"],
            "level": "WARNING",
            "propagate": False,
        },
        # Universal logger (entire project)
        "": {
            "handlers": ["app_file", "console"],
            "level": "INFO",
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "core.utils.pagination.CustomPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "core.api.exceptions.custom_exception_handler",  # noqa
}

AUTH_USER_MODEL = "account.User"  # noqa

UNFOLD = {
    "SITE_URL": "/admin/",
    "SITE_TITLE": "DJANGO REST Template",
    "SITE_HEADER": "DJANGO REST Template",
    "SITE_SUBHEADER": lambda request: (
        request.user.get_navigation_title() if request.user.is_authenticated else "Unknown User"
    ),
    "SIDEBAR": {
        "show_search": False,
    },
}

CORS_URLS_REGEX = r"^/api/.*$"
