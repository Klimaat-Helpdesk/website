from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from taggit.managers import TaggableManager
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.snippets.models import register_snippet

@register_snippet
class Expert(models.Model):
    """To split the users from the experts. Users, for the time being will be only those who
    have enough knowledge to interact with the website.
    """

    featured = models.BooleanField(default=False)
    name = models.CharField(_('name'), max_length=255, null=False, blank=False)
    email = models.EmailField(_('email'), null=True, blank=True)
    bio = models.TextField(verbose_name=_('biography'), null=False, blank=False)
    picture = models.ForeignKey('wagtailimages.Image', null=True, related_name='+', on_delete=models.SET_NULL)
    areas_expertise = TaggableManager(verbose_name=_('areas of expertise'))
    affiliation = models.CharField(_('Affiliation'), blank=False, max_length=128)
    website = models.URLField(_('Website'), blank=True)
    twitter_profile = models.CharField(_('Twitter Profile'), blank=True, null=True, max_length=50)
    linkedin_profile = models.CharField(_('LinkedIn Profile'), blank=True, null=True, max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel('featured'),
        FieldPanel('name'),
        ImageChooserPanel('picture'),
        FieldPanel('email'),
        FieldPanel('bio'),
        FieldPanel('affiliation'),
        FieldPanel('areas_expertise'),
        FieldPanel('website'),
        FieldPanel('twitter_profile'),
        FieldPanel('linkedin_profile'),
    ]

    def __str__(self):
        return f"{self.name}"

    def get_answered_questions(self):
        question_links = self.expert_answer_relationship.all()
        return [l.answer for l in question_links if l.answer is not None]

    def get_answer_categories(self):
        answers = self.get_answered_questions()
        categories = []
        for a in answers:
            categories += a.categories
        return categories



