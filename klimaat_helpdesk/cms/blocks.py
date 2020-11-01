from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class AnswerRichTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(features=(
        'h2',
        'h3',
        'h4',
        'bold',
        'italic',
        'ol',
        'ul',
        'hr',
        'link',
        'document-link',
        'embed',
        'superscript',
        'subscript',
    ))

    class Meta:
        icon = 'text'
        template = 'cms/blocks/rich_text.html'


class AnswerImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="The recommended aspect ratio is landscape with a size of of 1920x1080. Portrait images not recommended.")
    caption = blocks.CharBlock(max_length=2500)

    class Meta:
        icon = 'image'
        template = 'cms/blocks/image.html'


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(max_length=1000)

    class Meta:
        icon = 'text'
        template = 'cms/blocks/quote.html'


class ScientificSourceBlock(blocks.StructBlock):
    reference_text = blocks.TextBlock(max_length=2500)
    url_or_doi = blocks.TextBlock(max_length=2500)


class AnswerOriginBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    content = blocks.RichTextBlock(help_text="Clarification of the answer's origin")
    sources = blocks.ListBlock(ScientificSourceBlock)

    class Meta:
        icon = 'text'
        template = 'cms/blocks/answer_origin.html'


class RelatedItemsBlock(blocks.StructBlock):
    items = blocks.ListBlock(blocks.PageChooserBlock(page_type='cms.Answer'))

    class Meta:
        icon = 'text'
        template = 'cms/blocks/related_content.html'
