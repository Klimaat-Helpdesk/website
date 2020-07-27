from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class RichTextBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()

    class Meta:
        icon = 'text'
        template = 'cms/blocks/rich_text.html'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = 'image'
        template = 'cms/blocks/image.html'


class QuoteBlock(blocks.StructBlock):
    quote = blocks.CharBlock(max_length=1000)

    class Meta:
        icon = 'text'
        template = 'cms/blocks/quote.html'


class ScientificSourceBlock(blocks.StructBlock):
    reference_text = blocks.TextBlock(max_length=500)
    url_or_doi = blocks.TextBlock(max_length=500)


class AnswerOriginBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    content = blocks.RichTextBlock()
    sources = blocks.ListBlock(ScientificSourceBlock)

    class Meta:
        icon = 'text'
        template = 'cms/blocks/answer_origin.html'


class RelatedItemsBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255)
    items = blocks.ListBlock(blocks.PageChooserBlock(page_type='cms.Answer'))
