from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class ExpertAnswerRelationship(Orderable, models.Model):
    """Intermediate table for holding the many-to-many relationship in case there are many experts working on the same
    answer.
    """
    answer = ParentalKey('Answer', related_name='answer_expert_relationship', on_delete=models.CASCADE)
    expert = models.ForeignKey('experts.Expert', related_name='expert_answer_relationship', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('expert')
    ]


class AnswerTag(TaggedItemBase):
    content_object = ParentalKey('Answer', related_name='tagged_items', on_delete=models.CASCADE)


class AnswerCategory(models.Model):
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(
        verbose_name=_('slug'),
        allow_unicode=True,
        max_length=50,
        help_text=_('A slug to identify the category'))

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = _("Answer Category")
        verbose_name_plural = _("Answer Categories")
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(AnswerCategory)


class Answer(Page):
    template = 'cms/answer_detail.html'

    content = RichTextField()

    categories = ParentalManyToManyField('cms.AnswerCategory', blank=True)
    tags = ClusterTaggableManager(through=AnswerTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname='full'),
        MultiFieldPanel(
            [
                InlinePanel('answer_expert_relationship', label=_('Expert(s)'), panels=None, min_num=1)
            ],
            heading=_('Expert(s)')
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            ],
            heading=_("Categories")
        ),
        FieldPanel('tags'),
    ]

    @property
    def experts(self):
        experts = [
            n.expert for n in self.answer_expert_relationship.all()
        ]
        return experts

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags


class AnswerIndexPage(RoutablePageMixin, Page):
    """List of answers on the website
    """
    subtitle = models.TextField(help_text=_('Subtitle to show on the header of the page'))

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname='full')
    ]

    subpage_types = ['Answer']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerIndexPage, self).get_context(request, *args, **kwargs)

        all_answers = Answer.objects.descendant_of(self).live()
        paginator = Paginator(all_answers, 20)
        page = request.GET.get('page')
        try:
            answers = paginator.page(page)
        except PageNotAnInteger:
            answers = paginator.page(1)
        except EmptyPage:
            answers = paginator.page(paginator.num_pages)

        context.update({
            'answers': answers,
            'subtitle': self.subtitle,
            'paginator': paginator
        })

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        try:
            category = AnswerCategory.objects.get(slug=cat_slug)
        except AnswerCategory.DoesNotExist:
            return redirect('/')

        context.update({
            'answers': Answer.objects.live().public().filter(category__in=[category])
        })

        return render(request, 'cms/category_list.html', context)
