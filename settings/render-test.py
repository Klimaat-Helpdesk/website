import os

#from .base import *  #
#from .base import * #  NOQA
from .base import BASE_DIR, RELEASE_VERSION, WAGTAILADMIN_BASE_URL, DEFAULT_AUTO_FIELD,INSTALLED_APPS, ROOT_URLCONF, MANIFEST_LOADER, TEMPLATES, AUTH_USER_MODEL, DATABASES, SECRET_KEY,  AUTH_PASSWORD_VALIDATORS,LANGUAGE_CODE,TIME_ZONE,USE_I18N, USE_L10N , USE_TZ, STATICFILES_FINDERS, WAGTAIL_SITE_NAME
from pathlib import Path

#to_exclude = ['STORAGES']
#for name in to_exclude:
    #settings.base.globals().pop(name)
#delattr( ., "STORAGES")

def get_secret(secret_path, default=None):
    if not os.path.exists(secret_path):
        return default
    return Path(secret_path).read_text().strip()



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# Database setup
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "NAME": os.getenv("POSTGRES_NAME", "biodiversiteithelpdesk"),
        "HOST": os.getenv("POSTGRES_HOST", ""),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
        "USER": os.getenv("POSTGRES_USER", ""),
        "PASSWORD": get_secret(
            os.getenv("POSTGRES_PASSWORD_FILE", "/run/secrets/db_password"),
            "",
        ),
    }
}


ROOT_URLCONF = "urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail_helpdesk.utils.context_processors.defaults",
            ],
        },
    },
]

AUTH_USER_MODEL = "users.User"

# Allowed hosts and environment setup
DEBUG = False
ALLOWED_HOSTS = ["test.klimaathelpdesk.org"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Secrets
SECRET_KEY = get_secret(
    os.getenv("SECRET_KEY_FILE", "/run/secrets/secret_key"),
    "django-insecure-dev-key",
)

# Paths for static and media
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}


# Wagtail
WAGTAIL_SITE_NAME = "klimaat-helpdesk"
WAGTAILADMIN_BASE_URL = BASE_URL = "https://klimaathelpdesk.org"
