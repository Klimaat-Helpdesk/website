from django.db import models
from django.db.models import TextField
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel, HelpPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from config import settings
from klimaat_helpdesk.cms.blocks import AnswerRichTextBlock, QuoteBlock, AnswerImageBlock, AnswerOriginBlock, \
    RelatedItemsBlock
from klimaat_helpdesk.experts.models import Expert
from klimaat_helpdesk.volunteers.models import Volunteer


class ExpertAnswerRelationship(Orderable, models.Model):
    """
    Intermediate table for holding the many-to-many relationship in case there are
    many experts working on the same answer.
    """
    answer = ParentalKey('Answer', related_name='answer_expert_relationship', on_delete=models.CASCADE)
    expert = models.ForeignKey('experts.Expert', related_name='expert_answer_relationship', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('expert')
    ]


class CategoryAnswerRelationship(Orderable, models.Model):
    """
    Intermediate table for holding the many-to-many relationship between categories and answers
    """
    answer = ParentalKey('Answer', related_name='answer_category_relationship', on_delete=models.CASCADE)
    category = models.ForeignKey('cms.AnswerCategory', related_name='category_answer_relationship', on_delete=models.CASCADE)

    panels = [
        SnippetChooserPanel('category')
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

    def get_prefiltered_search_params(self):
        return "?{}=".format(self.name)

register_snippet(AnswerCategory)


class Answer(Page):
    template = 'cms/answer_detail.html'

    # Determines type and whether its highlighted in overview list
    type = models.CharField(
        choices=[('answer', 'Antwoord'), ('column', 'Column')],
        max_length=100,
        default='answer',
        help_text=_('Choose between answer or discussion piece with a more prominent look')
    )
    featured = models.BooleanField(default=False)

    content = RichTextField(blank=True)
    excerpt = models.CharField(
        verbose_name=_('Short description'),
        max_length=255,
        blank=False,
        null=True,
        help_text=_('This helps with search engines and when sharing on social media'),
    )
    introduction = TextField(
        verbose_name=_('Introduction'),
        default='',
        blank=True,
        null=True,
        help_text=_('This text is displayed above the tags, useful as a TLDR section'),
    )
    tags = ClusterTaggableManager(through=AnswerTag, blank=True)

    social_image =  models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('This is the image that will be displayed when sharing on social media'),
    )

    # Freeform content of answer
    page_content = StreamField([
        ('richtext', AnswerRichTextBlock()),
        ('image', AnswerImageBlock()),
        ('quote', QuoteBlock()),
    ])

    # Which experts and how was this answered?
    answer_origin = StreamField([
        ('origin', AnswerOriginBlock())
        ], blank=True)

    # Related items
    related_items = StreamField([
        ('related_items', RelatedItemsBlock())
        ], blank=True)

    parent_page_types = ['AnswerIndexPage']

    content_panels = Page.content_panels + [
        FieldPanel('type'),

        FieldPanel('featured',
                   heading=_("Show this answer on the home page")),

        FieldPanel('excerpt',
                   classname='full',),

        FieldPanel('introduction', classname='full'),

        MultiFieldPanel(
            [
                InlinePanel('answer_category_relationship', label=_('Categorie(n)'), panels=None, min_num=1)
            ],
            heading=_('Categorie(s)')
        ),
        FieldPanel('tags', heading="Please use tags with a maximum length of 16 characters per single word to avoid overlap in the mobile view."),
        MultiFieldPanel(
            [
                InlinePanel('answer_expert_relationship', label=_('Expert(s)'), panels=None, min_num=1)
            ],
            heading=_('Expert(s)')
        ),
        StreamFieldPanel('page_content'),
        StreamFieldPanel('answer_origin'),
        StreamFieldPanel('related_items'),
        ImageChooserPanel('social_image', help_text=_('Image to be used when sharing on social media')),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('page_content'),
    ]

    @property
    def experts(self):
        experts = [
            n.expert for n in self.answer_expert_relationship.all()
        ]
        return experts

    @property
    def categories(self):
        categories = [
            n.category for n in self.answer_category_relationship.all()
        ]
        return categories

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

    def get_references(self):
        """
        Build reference list, in the order Wagtail returns them.  ### , alphabetically to sort of comply with standards

        TODO: References for articles can be separated from the origin and make them a proper ListBlock that can be
            handled by editors as they see fit. Having the references within a StreamField of 'origins' seems counter
            intuitive.

        """
        ref_list = []
        try:
            component = self.answer_origin[0]
        except IndexError:
            return ref_list

        # Access streamfield elements
        for element in component.value['sources']:
            ref_list.append({
                'text' : element['reference_text'],
                'url' : element['url_or_doi'],
            })

        # Sort by text starting letter, best we can do for now
        # ref_list.sort(key=lambda e: e['text'])
        return ref_list

    def get_primary_expert(self):
        """
        Gets the first expert associated with this answer if it exists.
        """
        try:
            first = self.experts[0]
        except IndexError:
            return _('Unknown')
        else:
            return first

    def get_all_categories(self):
        return [{
            'title': c.name,
            'url': c.get_prefiltered_search_params()
        } for c in self.categories]

    def get_card_data(self):
        return {
            'title' : self.title,
            'url' : self.url,
            'author' : self.get_primary_expert(),
            'categories': self.get_all_categories(),
            'type': 'answer'
        }

    def get_as_overview_row_card(self):
        if self.type == 'answer':
            return render_to_string('core/includes/answer_block.html',
                                    context=self.get_card_data())
        else: # It's a column
            return render_to_string('core/includes/column_block.html',
                                    context=self.get_card_data())

    def get_as_home_row_card(self):
        return render_to_string('core/includes/answer_home_block.html',
                                context=self.get_card_data())

    def get_as_related_row_card(self):
        return render_to_string('core/includes/related_item_block.html',
                                context=self.get_card_data())

    def get_context(self, request, *args, **kwargs):
        context = super(Answer, self).get_context(request, *args, **kwargs)

        categories = AnswerCategory.objects.all()

        context.update({
            'categories': categories,
            'answers_page': AnswerIndexPage.objects.first().url,
            'experts_page': ExpertIndexPage.objects.first(),
        })
        return context

    class Meta:
        ordering = ['-first_published_at', ]


class AnswerIndexPage(RoutablePageMixin, Page):
    """List of answers on the website
    """
    template = 'cms/answers_list.html'

    subpage_types = ['Answer']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request, *args, **kwargs):
        context = super(AnswerIndexPage, self).get_context(request, *args, **kwargs)

        answers = Answer.objects.descendant_of(self).live().filter(type='answer').specific().order_by('-first_published_at')
        columns = Answer.objects.live().filter(type='column').specific().order_by('-first_published_at')

        # Filter categories based on GET params
        chosen_categories = []
        for filter in request.GET:
            try:
                category = AnswerCategory.objects.get(name__iexact=filter)
            except AnswerCategory.DoesNotExist:
                # In case someone puts weird stuff in the url
                pass
            else:
                chosen_categories.append(category)

        if len(chosen_categories) > 0:
            answers = answers.filter(answer_category_relationship__category__in=chosen_categories)
            columns = columns.filter(answer_category_relationship__category__in=chosen_categories)

        # Adjust categories to maintain checked status
        categories = AnswerCategory.objects.all()
        categories_context = [
          {
                'category' : c,
                'selected' : True if c in chosen_categories else False
          } for c in categories
        ]

        # Insert column every 3 answers
        answers_and_columns = list(answers)
        if len(columns) > 0:
            # INTERSPACING = len(answers) // len(columns) # Can be used to spread evenly if desired
            INTERSPACING = 3
            if len(answers) >= INTERSPACING:
                column_index = 0
                for index in range(len(answers)):
                    if index != 0 and index % INTERSPACING == 0:
                        try:
                            answers_and_columns.insert(index + column_index, columns[column_index])
                        except IndexError:
                            break
                        else:
                            column_index += 1
            # List is too short, cannot interspace, so just put them at the end
            else:
                answers_and_columns += list(columns)

        context.update({
            'answers_page': AnswerIndexPage.objects.first().url,
            'categories': categories_context,
            'answers_and_columns': answers_and_columns,
            'experts_page': ExpertIndexPage.objects.first(),
        })
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
    intro = RichTextField(blank=True)
    outro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro'),
        FieldPanel('outro'),
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


class VolunteerIndexPage(Page):
    """ List of volunteers on the website """
    template = 'volunteers/volunteers_list.html'
    subtitle = models.CharField(max_length=128, blank=False)
    intro = RichTextField(blank=True)
    outro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro'),
        FieldPanel('outro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(VolunteerIndexPage, self).get_context(request, *args, **kwargs)
        volunteers = Volunteer.objects.all()

        context.update({
            'volunteers': volunteers,
            'answers_page': AnswerIndexPage.objects.first().url,
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
