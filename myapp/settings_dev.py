from .settings_base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

SECURE_SSL_REDIRECT=False

INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CORS_ALLOW_ALL_ORIGINS = True

# Auto-reconnect on startup
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# Development settings (run tasks locally, no need for concurrency)
CELERY_BROKER_URL="sqla+sqlite:///celerydb.sqlite3"
CELERY_RESULT_BACKEND="django-db"
CELERY_TASK_ALWAYS_EAGER = True  # Runs tasks locally
CELERYD_POOL = 'solo'  # For Windows, avoids multiprocessing (development only)