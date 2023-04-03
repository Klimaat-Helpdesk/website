from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = User.objects.make_random_password()
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ["username"]
