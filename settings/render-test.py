import os
import dj_database_url 
from .base import *  # NOQA


INSTALLED_APPS += [
    # "debug_toolbar",
]

MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware"
]

# Replace the SQLite DATABASES configuration with PostgreSQL:
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        #default='postgresql://klimaathelpdeskdev_user:jRrv7yfoUkVI5Xt437CU43PS9SfXEHlo@dpg-cvr7nsvgi27c738n8log-a.frankfurt-postgres.render.com/klimaathelpdeskdev',
        default='postgresql://klimaathelpdeskdev_user:jRrv7yfoUkVI5Xt437CU43PS9SfXEHlo@dpg-cvr7nsvgi27c738n8log-a/klimaathelpdeskdev',
        conn_max_age=600
    )
}

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS.append("test.klimaathelpdesk.org")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGEME!!!"

BASE_URL = WAGTAILADMIN_BASE_URL = "http://localhost:8000"
MEDIA_ROOT = "/media"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
MEDIA_ROOT = "/media"

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WAGTAIL_SITE_NAME = "klimaat-helpdesk"

try:
    from .local import *  # NOQA
except ImportError:
    pass
