from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class ExpertAnswerRelationship(Orderable, models.Model):
    """Intermediate table for holding the many-to-many relationship in case there are many experts working on the same
    answer.
    """
    answer = ParentalKey('Answer', related_name='answer_expert_relationship', on_delete=models.CASCADE)
    expert = models.ForeignKey('experts.Expert', related_name='expert_answer_relationship', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('expert')
    ]


class Answer(Page):
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content', classname='full'),
        InlinePanel('answer_expert_relationship', label=_('Expert(s)'), panels=None, min_num=1),
    ]
