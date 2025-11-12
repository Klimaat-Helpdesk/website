import os

#from .base import *  #
#from .base import * #  NOQA
from .base import BASE_DIR, RELEASE_VERSION, WAGTAILADMIN_BASE_URL, DEFAULT_AUTO_FIELD,INSTALLED_APPS, ROOT_URLCONF, MANIFEST_LOADER, TEMPLATES, AUTH_USER_MODEL, DATABASES, SECRET_KEY,  AUTH_PASSWORD_VALIDATORS,LANGUAGE_CODE,TIME_ZONE,USE_I18N, USE_L10N , USE_TZ, STATICFILES_FINDERS, WAGTAIL_SITE_NAME #  NOQA

#to_exclude = ['STORAGES']
#for name in to_exclude:
    #settings.base.globals().pop(name)
#delattr( ., "STORAGES")

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

DEBUG = False
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS.append("test.klimaathelpdesk.org")

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

# Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


