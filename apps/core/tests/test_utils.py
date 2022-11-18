import os
from unittest.mock import patch

import pytest
from django.core.exceptions import ImproperlyConfigured

from apps.core.utils import check_for_debug_settings_in_production


def test_check_for_debug_settings_in_production(settings):
    settings.DEBUG = False
    with patch.dict(os.environ, {"DJANGO_SETTINGS_MODULE": "settings.production"}):
        check_for_debug_settings_in_production(), (
            "No error should be raised when DEBUG is set to False while "
            "production settings are active"
        )
        settings.DEBUG = True
        with pytest.raises(
            ImproperlyConfigured, match="Running production settings with DEBUG = True"
        ):
            check_for_debug_settings_in_production(), (
                "An error should be raised when DEBUG is set to True while "
                "production settings are active"
            )
    with patch.dict(os.environ, {"DJANGO_SETTINGS_MODULE": "settings.development"}):
        check_for_debug_settings_in_production(), (
            "No error should be raised when DEBUG is set to False while "
            "development settings are active"
        )
        settings.DEBUG = True
        check_for_debug_settings_in_production(), (
            "No error should be raised when DEBUG is set to True while "
            "development settings are active"
        )
