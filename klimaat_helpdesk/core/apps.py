from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'klimaat_helpdesk.core'
    verbose_name = _('Core App')
