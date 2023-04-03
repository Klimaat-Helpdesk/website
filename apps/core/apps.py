from django.apps import AppConfig

from apps.core.utils import check_for_debug_settings_in_production


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        check_for_debug_settings_in_production()
