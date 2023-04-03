from .base import *  # noqa: F403

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = False

MANIFEST_LOADER["cache"] = True

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "formatters": {
        "default": {
            "verbose": "[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s"
        }
    },
    "loggers": {
        "klimaat-helpdesk": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "formatter": "verbose",
        },
        "wagtail": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "formatter": "verbose",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
            "formatter": "verbose",
        },
        "django.security": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
            "formatter": "verbose",
        },
    },
}

# Security settings as recommended by `manage check --deploy`
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Enable SECURE_HSTS_SECONDS only when the domain is definitive
# SECURE_HSTS_SECONDS = 3600 * 24 * 365  # 1 year

try:
    from .local import *
except ImportError:
    pass
