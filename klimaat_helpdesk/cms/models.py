from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.db.models import TextField
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from klimaat_helpdesk.experts.models import Expert


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
    description = models.CharField(_('description'), max_length=255, blank=False, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
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

    introduction = TextField(default='', blank=True, null=True)
    content = RichTextField()

    excerpt = models.CharField(verbose_name=_('Short description'), max_length=255, blank=False, null=True)
    category = models.ForeignKey(AnswerCategory, related_name='answers', on_delete=models.SET_NULL, null=True, default=None)
    tags = ClusterTaggableManager(through=AnswerTag, blank=True)

    parent_page_types = ['AnswerIndexPage']

    content_panels = Page.content_panels + [
        FieldPanel('excerpt', classname='full'),
        FieldPanel('introduction', classname='full'),
        FieldPanel('content', classname='full'),
        MultiFieldPanel(
            [
                InlinePanel('answer_expert_relationship', label=_('Expert(s)'), panels=None, min_num=1)
            ],
            heading=_('Expert(s)')
        ),
        MultiFieldPanel(
            [
                FieldPanel('category'),
            ],
            heading=_("Categories")
        ),
        FieldPanel('tags'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('content'),
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

    def get_context(self, request, *args, **kwargs):
        context = super(Answer, self).get_context(request, *args, **kwargs)

        categories = AnswerCategory.objects.all()

        context.update({
            'categories': categories,
            'answers_page': AnswerIndexPage.objects.first().url,
            'experts_page': ExpertIndexPage.objects.first(),
        })
        return context


class AnswerIndexPage(RoutablePageMixin, Page):
    """List of answers on the website
    """
    template = 'cms/answers_list.html'

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

        categories = AnswerCategory.objects.all()
        expert = Expert.objects.last()

        context.update({
            'answers_page': AnswerIndexPage.objects.first().url,
            'categories': categories,
            'answers': answers,
            'subtitle': self.subtitle,
            'experts_page': ExpertIndexPage.objects.first(),
            'expert': expert,
            'paginator': paginator
        })
        print(context)
        return context

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        try:
            category = AnswerCategory.objects.get(slug=cat_slug)
        except AnswerCategory.DoesNotExist:
            return redirect('/')

        context.update({
            'answers': Answer.objects.live().public().filter(category=category),
            'subtitle': category.description,
        })

        return render(request, self.template, context)


class ExpertIndexPage(Page):
    """ List of experts on the website """
    template = 'experts/experts_list.html'
    subtitle = models.CharField(max_length=128, blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(ExpertIndexPage, self).get_context(request, *args, **kwargs)
        experts = Expert.objects.all()
        categories = AnswerCategory.objects.all()

        context.update({
            'experts': experts,
            'answers_page': AnswerIndexPage.objects.first().url,
            'categories': categories,

        })
        return context


class GeneralPage(Page):
    """ A page that won't show sidebar. Ideal for privacy policy, etc. """
    template = 'cms/general_page.html'
    subtitle = models.CharField(max_length=128, blank=True)

    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('content')
    ]
