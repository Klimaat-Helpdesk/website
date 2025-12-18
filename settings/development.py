from .base import *  # NOQA


INSTALLED_APPS += [
    # "debug_toolbar",
]

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGEME!!!"

BASE_URL = WAGTAILADMIN_BASE_URL = "http://localhost:8000"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
}

# Django should serve static, frontend service (npm run start) will auto rebuild
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
}
STATIC_URL = "/static/"
STATIC_ROOT = "/static/"

# Project has no docker-compose, use filesystem for media
STORAGES["default"] = {  # noqa: F405
    "BACKEND": "django.core.files.storage.FileSystemStorage"
}
MEDIA_ROOT = os.getenv("MEDIA_ROOT", BASE_DIR / "media")
MEDIA_URL = "/media/"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

