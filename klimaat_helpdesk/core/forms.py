from django import forms
from django.utils.translation import gettext_lazy as _

from klimaat_helpdesk.core.models import Question


class AskQuestion(forms.ModelForm):
    accept_terms = forms.BooleanField(label=_('Accept Terms & Conditions'), required=True)

    class Meta:
        model = Question
        fields = ['user_email', 'question']
