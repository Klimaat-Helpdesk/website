from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail_helpdesk.core.models import Question

from .models import GitlabIssue


@receiver(post_save, sender=Question)
def create_gitlab_issue(sender, instance, created, *args, **kwargs):
    """
    Signal to create a Gitlab issue when a new Question is approved.
    """
    try:
        settings.GITLAB_PERSONAL_TOKEN
    except AttributeError:
        # GITLAB_PERSONAL_TOKEN setting was missing
        return

    try:
        instance.issue
    except ObjectDoesNotExist:
        if instance.status == instance.APPROVED:
            GitlabIssue.objects.create(question=instance)
