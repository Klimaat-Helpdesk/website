# render test settings for Django project on Render.com by Jos Velema
# did not succeed , something with static files and storage

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------
# Helpers
# -------------------------
def read_secret_file(path: str | None, default: str = "") -> str:
    """Read plaintext secret file (Render secret files live in /etc/secrets/)."""
    if not path:
        return default
    try:
        p = Path(path)
        return p.read_text(encoding="utf-8").strip() if p.exists() else default
    except Exception:
        return default


# -------------------------
# Core Django/Wagtail apps
# -------------------------
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


# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # required for static files on Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


# -------------------------
# Basic project settings
# -------------------------
DEBUG = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "urls"
AUTH_USER_MODEL = "users.User"

ALLOWED_HOSTS = ["test.klimaathelpdesk.org"]
_render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if _render_host:
    ALLOWED_HOSTS.append(_render_host)

CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

SECRET_KEY = (
    read_secret_file(os.getenv("SECRET_KEY_FILE", "/etc/secrets/secret_key"))
    or os.getenv("DJANGO_SECRET_KEY", "django-insecure-dev-key")
)

WAGTAIL_SITE_NAME = "klimaat-helpdesk"
WAGTAILADMIN_BASE_URL = BASE_URL = os.getenv(
    "WAGTAILADMIN_BASE_URL", "https://test.klimaathelpdesk.org"
)


# -------------------------
# Database
# -------------------------
DB_PASSWORD = (
    os.getenv("POSTGRES_PASSWORD")
    or read_secret_file(os.getenv("POSTGRES_PASSWORD_FILE", "/etc/secrets/db_password"))
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_NAME", "klimaathelpdesk"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": int(os.getenv("POSTGRES_PORT", "5432")),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": DB_PASSWORD,
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,
        # Uncomment als jouw Render DB SSL eist:
        # "OPTIONS": {"sslmode": os.getenv("POSTGRES_SSLMODE", "require")},
    }
}


# -------------------------
# Templates
# -------------------------
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


# -------------------------
# Static & Media (Render)
# -------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# -------------------------
# Email & Logging
# -------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
