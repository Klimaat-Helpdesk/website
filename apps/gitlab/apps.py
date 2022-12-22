from django.apps import AppConfig


class GitlabAppConfig(AppConfig):
    name = "apps.gitlab"

    def ready(self):
        import apps.gitlab.signals  # noqa: F401
