from django import forms
from django.utils.translation import gettext_lazy as _

from klimaat_helpdesk.cms.models import AnswerCategory
from klimaat_helpdesk.core.models import Question


class AskQuestion(forms.ModelForm):
    accept_terms = forms.BooleanField(label=_('Accept Terms & Conditions'), required=True)

    class Meta:
        model = Question
        fields = ['user_email', 'question']


class ClimateQuestion(forms.Form):
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                              choices=AnswerCategory.objects.all())
    main_question = forms.CharField(max_length=1000)
    relevant_location = forms.CharField(max_length=1000)
    relevant_timespan = forms.CharField(max_length=1000)
    extra_info = forms.CharField(max_length=5000)
    accept_terms = forms.BooleanField(label=_('Accept Terms & Conditions'), required=True)
