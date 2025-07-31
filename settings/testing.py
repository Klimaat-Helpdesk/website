from .base import *  # NOQA


SECRET_KEY = "CHANGEME!!!"

# We need this because django-webtest uses StaticFilesStorage
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
}
STATIC_URL = "/static/"
STATIC_ROOT = "/static/"

# Project has no docker-compose, use filesystem for media
STORAGES["default"] = {  # noqa: F405
    "BACKEND": "django.core.files.storage.FileSystemStorage"
}
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
