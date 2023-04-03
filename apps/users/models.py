from logging import getLogger

from django.contrib.auth.models import AbstractUser, Group
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

logger = getLogger(__name__)


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        group = Group.objects.get(name="Editors")
        group.user_set.add(instance)
    except Group.DoesNotExist:
        logger.info("Group Editor does not exist")
