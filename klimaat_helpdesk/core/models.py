from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _
import gitlab
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet


class Question(models.Model):
    """Main element to drive the flow of the website. Questions are what the user can ask and which will trigger the
    rest of the actions on the website
    """
    question = models.TextField(verbose_name=_('Your Question'), blank=False, null=False)
    user_email = models.EmailField(verbose_name=_('User Email'), blank=True, null=True)
    asked_by_ip = models.GenericIPAddressField(null=True, blank=True)

    date_asked = models.DateTimeField(auto_now_add=True)
    approved = models.NullBooleanField(default=None)

    def save(self, **kwargs):
        try:
            self.issue
        except ObjectDoesNotExist:
            if self.approved:
                GitlabIssues.objects.create(question=self)
        super().save(**kwargs)


class GitlabIssues(models.Model):
    question = models.OneToOneField(Question, on_delete=models.SET_NULL, null=True, related_name='issue')
    issue_id = models.IntegerField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.issue_id is None:
            if not settings.DEBUG:
                gl = gitlab.Gitlab('https://gitlab.com', private_token=settings.GITLAB_PERSONAL_TOKEN)
                project = gl.projects.get(settings.GITLAB_PROJECT_ID)
                template_issue = project.files.get(
                    file_path='Templates/template_question_issue.md', ref='master').decode().decode('utf-8')

                issue = project.issues.create({
                    'title': f'Question: {self.question.question}',
                    'description': template_issue
                })
                issue.labels = ['Answer in progress']
                issue.save()
                self.issue_id = issue.get_id()
            else:
                self.issue_id = 1234
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


@register_snippet
class FooterText(models.Model):
    text = RichTextField(blank=False)

    panels = [
        FieldPanel('text'),
    ]

    class Meta:
        verbose_name_plural = 'Footer Text'

    def __str__(self):
        return "Footer Text"
