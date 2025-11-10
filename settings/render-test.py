import os
import dj_database_url 
from pathlib import Path


def get_secret(secret_path, default=None):
    if not os.path.exists(secret_path):
        return default
    return Path(secret_path).read_text().strip()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
INSTALLED_APPS = [
    "apps.gitlab",
    "apps.users",
    "apps.frontend",
    "wagtail_helpdesk",
    "wagtail_helpdesk.cms",
    "wagtail_helpdesk.core",
    "wagtail_helpdesk.experts",
    "wagtail_helpdesk.utils",
    "wagtail_helpdesk.volunteers",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.table_block",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]


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


DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,  # For PgBouncer
        "NAME": os.getenv("POSTGRES_NAME", "biodiversiteithelpdesk"),
        "HOST": os.getenv("POSTGRES_HOST", ""),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
        "USER": os.getenv("POSTGRES_USER", ""),
        "PASSWORD": get_secret(
            os.getenv("POSTGRES_PASSWORD_FILE", "/run/secrets/db_password"),
            "",
        ),
}}

# Set default primary key field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "urls"

MANIFEST_LOADER = {
    "output_dir": BASE_DIR / "apps" / "frontend" / "static",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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
ALLOWED_HOSTS = []
DEBUG = True
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS.append("test.klimaathelpdesk.org")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGEME!!!"

BASE_URL = WAGTAILADMIN_BASE_URL = "http://localhost:8000"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

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
WAGTAILADMIN_BASE_URL = BASE_URL = "https://klimaathelpdesk.org"


