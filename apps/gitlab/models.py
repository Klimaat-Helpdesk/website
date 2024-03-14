import gitlab
from django.conf import settings
from django.db import models
from wagtail_helpdesk.core.models import Question


class GitlabIssue(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.SET_NULL, null=True, related_name="issue"
    )
    issue_id = models.IntegerField(null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.issue_id is None:
            if not settings.DEBUG:
                gl = gitlab.Gitlab(
                    "https://gitlab.com", private_token=settings.GITLAB_PERSONAL_TOKEN
                )
                project = gl.projects.get(settings.GITLAB_PROJECT_ID)
                template_issue = (
                    project.files.get(
                        file_path="Templates/template_question_issue.md", ref="master"
                    )
                    .decode()
                    .decode("utf-8")
                )

                issue_body = (
                    f"Question: {self.question.question}\n"
                    f"Original Question: {self.question.original_question}\n\n"
                    f"- Categories: {self.question.categories}\n"
                    f"- Timespan: {self.question.relevant_timespan}\n"
                    f"- Location: {self.question.relevant_location}\n"
                    f"- Extra information: {self.question.extra_info}\n"
                    f"- Asked by: {self.question.user_email}\n"
                    f"\n\n{template_issue}"
                )
                issue_title = f"Question: {self.question.question}"
                issue = project.issues.create(
                    {
                        "title": issue_title[:254],
                        "description": issue_body,
                    }
                )
                issue.labels = [
                    "Inbox",
                ]
                issue.save()
                self.issue_id = issue.get_id()
            else:
                self.issue_id = 1234

        super().save(*args, **kwargs)
