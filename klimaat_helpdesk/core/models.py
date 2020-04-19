from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    """Main element to drive the flow of the website. Questions are what the user can ask and which will trigger the
    rest of the actions on the website
    """
    question = models.TextField(verbose_name=_('Your Question'), blank=False, null=False)
    user_email = models.EmailField(verbose_name=_('User Email'), blank=True, null=True)
    asked_by_ip = models.GenericIPAddressField(null=True, blank=True)

    date_asked = models.DateTimeField(auto_now_add=True)
    approved = models.NullBooleanField(default=None)

