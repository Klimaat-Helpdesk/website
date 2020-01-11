from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExpertsConfig(AppConfig):
    name = "klimaat_helpdesk.experts"
    verbose_name = _("Experts")
