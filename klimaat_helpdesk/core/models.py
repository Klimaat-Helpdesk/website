from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
import gitlab


class Question(models.Model):
    """Main element to drive the flow of the website. Questions are what the user can ask and which will trigger the
    rest of the actions on the website
    """
    UNDECIDED = 0
    APPROVED = 1
    ANSWERED = 2
    REJECTED = 3

    STATUS_CHOICES = (
        (UNDECIDED, _('Undecided')),
        (APPROVED, _('Approved')),
        (ANSWERED, _('Answered')),
        (REJECTED, _('Rejected'))
    )

    question = models.TextField(verbose_name=_('Your Question'), blank=False, null=False)
    original_question = models.TextField(verbose_name=_('Backup information'), blank=True, null=True)
    relevant_timespan = models.TextField(verbose_name=_('Relevant timespan'), blank=True, null=True)
    relevant_location = models.TextField(verbose_name=_('Relevant location'), blank=True, null=True)
    extra_info = models.TextField(verbose_name=_('Extra information'), blank=True, null=True)
    categories = models.TextField(verbose_name=_('Categories'), blank=True, null=True)

    user_email = models.EmailField(verbose_name=_('User Email'), blank=True, null=True)
    asked_by_ip = models.GenericIPAddressField(null=True, blank=True)

    date_asked = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNDECIDED)

    def get_card_data(self):
        return {
            'title': self.question,
        }

    def get_as_home_row_card(self):
        return render_to_string('core/includes/question_list_block.html',
                                context=self.get_card_data())

    def save(self, **kwargs):
        super().save(**kwargs)
        try:
            self.issue
        except ObjectDoesNotExist:
            if self.approved or self.status == self.APPROVED:
                GitlabIssues.objects.create(question=self)



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

                issue_body = f"Question: {self.question.question}\n" \
                             f"Original Question: {self.question.original_question}\n\n" \
                             f"- Categories: {self.question.categories}\n" \
                             f"- Timespan: {self.question.relevant_timespan}\n" \
                             f"- Location: {self.question.relevant_location}\n" \
                             f"- Extra information: {self.question.extra_info}\n" \
                             f"- Asked by: {self.question.user_email}\n" \
                             f"\n\n{template_issue}"
                issue_title = f"Question: {self.question.question}"
                issue = project.issues.create({
                    'title': issue_title[:254],
                    'description': issue_body,
                })
                issue.labels = ['Editor needed', ]
                issue.save()
                self.issue_id = issue.get_id()
            else:
                self.issue_id = 1234
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
