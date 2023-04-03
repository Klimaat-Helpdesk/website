import os

from django.conf import ENVIRONMENT_VARIABLE, settings
from django.core.exceptions import ImproperlyConfigured


def check_for_debug_settings_in_production():
    settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
    if settings_module.endswith("production") and settings.DEBUG:
        raise ImproperlyConfigured("Running production settings with DEBUG = True")
