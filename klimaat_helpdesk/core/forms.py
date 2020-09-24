from django import forms
from django.utils.translation import gettext_lazy as _

from klimaat_helpdesk.cms.models import AnswerCategory


class TagWidget(forms.CheckboxSelectMultiple):
    option_template_name = 'core/forms/tag_option.html'


class ClimateQuestionForm(forms.Form):
    """
    Form used when users ask a new question. Fields are combined into
    one field for the GitLab integration.
    """
    categories = forms.MultipleChoiceField(widget=TagWidget,
                              choices=[(c.name, c.name) for c in AnswerCategory.objects.all()], required=False)
    main_question = forms.CharField(max_length=1000, required=True, label='Mijn vraag is*')
    relevant_location = forms.CharField(max_length=1000, required=False, label='Locatie (bijvoorbeeld Amsterdam of Europa)')
    relevant_timespan = forms.CharField(max_length=1000, required=False, label='Tijdperk (bijvoorbeeld de komende 10 jaar)')
    extra_info = forms.CharField(max_length=5000, required=False, label='Aanvullende informatie')
    # accept_terms = forms.BooleanField(label=_('Ik ga ermee akkoord dat mijn vraag op klimaathelpdesk.nl gepubliceerd wordt.'), required=True)


class ClimateQuestionUserContactForm(forms.Form):
    """
    Form used to allow users to give their email address, this will
    update the question they asked before. Not a required step.
    """
    user_email = forms.EmailField(required=True)
    accept_terms = forms.BooleanField(label=_('Accept Terms & Conditions'), required=True)
