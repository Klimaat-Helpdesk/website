"""
Django settings for klimaat-helpdesk project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from botocore.client import Config as BotoConfig


def get_secret(secret_path, default=None):
    if not os.path.exists(secret_path):
        return default
    return Path(secret_path).read_text().strip()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

# https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
# Allow localhost for docker HEALTHCHECK
ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]"] + list(filter(None, os.getenv("ALLOWED_HOSTS", "").split(",")))

RELEASE_VERSION = os.getenv("RELEASE_VERSION", "NO VERSION FOUND")
WAGTAILADMIN_BASE_URL=os.getenv("WAGTAILADMIN_BASE_URL")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "info@klimaathelpdesk.org"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host

EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_secret(
    os.getenv("EMAIL_HOST_PASSWORD_FILE", "/run/secrets/email_host_password"),
    "",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() in ("true", "1")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-ssl
EMAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1")

# Set default primary key field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

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

    # Health check
    #"health_check",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

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

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
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

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret(
    os.getenv("SECRET_KEY_FILE", "/run/secrets/secret_key"),
    "django-insecure-default-secret-key",
)
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# S3/Minio (used by static and media storage)
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL", "http://minio:8001/")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "s3bucket")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_ACCESS_KEY = get_secret(
    os.getenv("AWS_SECRET_ACCESS_KEY_FILE", "/run/secrets/aws_secret_access_key"),
    "miniopassword",
)
# Fix SignatureDoesNotMatch with latest boto3 release:
# https://github.com/jschneier/django-storages/issues/1482#issuecomment-2648033009
AWS_S3_CLIENT_CONFIG = BotoConfig(
    request_checksum_calculation="when_required",
    response_checksum_validation="when_required",
)

# STORAGES
# https://docs.djangoproject.com/en/4.2/ref/settings/#storages
STORAGES = {
    "default": {"BACKEND": "apps.core.storages.MediaS3Storage"},
    "staticfiles": {"BACKEND": "apps.core.storages.StaticS3Storage"},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Wagtail settings

WAGTAIL_SITE_NAME = "klimaat-helpdesk"
