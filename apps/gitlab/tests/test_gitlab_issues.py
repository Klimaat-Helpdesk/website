import base64

import pytest
import responses
from wagtail_helpdesk.tests.factories import QuestionFactory

from apps.gitlab.models import GitlabIssue

pytestmark = pytest.mark.django_db


@responses.activate
def test_question_creates_gitlab_issue(settings):
    MOCK_PROJECT_ID = 12345
    MOCK_ISSUE_ID = 6789

    settings.GITLAB_PERSONAL_TOKEN = "fake-token"
    settings.GITLAB_PROJECT_ID = MOCK_PROJECT_ID

    responses.get(
        f"https://gitlab.com/api/v4/projects/{MOCK_PROJECT_ID}",
        json={"id": MOCK_PROJECT_ID},
    )

    responses.get(
        f"https://gitlab.com/api/v4/projects/{MOCK_PROJECT_ID}/repository/files/Templates%2Ftemplate_question_issue.md?ref=master",  # noqa: E501
        json={"content": base64.b64encode(b"fake template").decode()},
    )

    responses.post(
        f"https://gitlab.com/api/v4/projects/{MOCK_PROJECT_ID}/issues",
        json={"iid": MOCK_ISSUE_ID},
    )

    responses.put(
        f"https://gitlab.com/api/v4/projects/{MOCK_PROJECT_ID}/issues/{MOCK_ISSUE_ID}",
        json={"iid": MOCK_ISSUE_ID},
    )

    issue_count = GitlabIssue.objects.count()

    question = QuestionFactory()
    question.status = question.APPROVED
    question.save()

    assert GitlabIssue.objects.count() == issue_count + 1
    assert GitlabIssue.objects.filter(issue_id=MOCK_ISSUE_ID).exists()
