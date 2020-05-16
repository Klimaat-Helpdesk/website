from django import template

from klimaat_helpdesk.core.models import FooterText

register = template.Library()


@register.inclusion_tag('core/includes/footer_text.html', takes_context=True)
def get_footer(context):
    try:
        footer_text = FooterText.objects.first().text
    except AttributeError:
        footer_text = None
    return {'footer_text': footer_text}
