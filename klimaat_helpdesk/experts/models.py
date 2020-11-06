from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

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
    twitter_profile = models.URLField(_('Twitter Profile'), blank=True, null=True)
    linkedin_profile = models.URLField(_('LinkedIn Profile'), blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel('featured', heading="Show this expert on the home page, 3 experts recommended"),
        FieldPanel('name'),
        ImageChooserPanel('picture', heading="Expert's photo, 1:1 aspect ratio (square) works best"),
        FieldPanel('email'),
        FieldPanel('bio'),
        FieldPanel('affiliation'),
        FieldPanel('areas_expertise', heading="Areas of expertise. A maximum of 16 characters per word is recommended for optimal mobile display"),
        FieldPanel('website'),
        FieldPanel('twitter_profile'),
        FieldPanel('linkedin_profile'),
    ]

    def __str__(self):
        return f"{self.name}"

    def get_answered_questions(self):
        question_links = self.expert_answer_relationship.all()
        return [l.answer for l in question_links if l.answer is not None and l.answer.live]

    def get_answer_categories(self):
        answers = self.get_answered_questions()
        categories = set()
        for a in answers:
            categories |= set(a.categories)  # Using sets to avoid duplicates
        return categories

    @property
    def twitter_username(self):
        if self.twitter_profile:
            if self.twitter_profile.endswith('/'):
                self.twitter_profile = self.twitter_profile[:-1]
                self.save()
            twitter_username = self.twitter_profile.split('/')[-1]
            return twitter_username

    class Meta:
        ordering = ['name', ]


