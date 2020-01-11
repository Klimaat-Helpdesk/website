from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmsConfig(AppConfig):
    name = "klimaat_helpdesk.cms"
    verbose_name = _("Q&A CMS")
