from django import forms
from django.utils.translation import gettext_lazy as _

from klimaat_helpdesk.cms.models import AnswerCategory
from klimaat_helpdesk.core.models import Question


class TagWidget(forms.CheckboxSelectMultiple):
    option_template_name = 'core/forms/tag_option.html'


class AskQuestion(forms.ModelForm):
    accept_terms = forms.BooleanField(label=_('Accept Terms & Conditions'), required=True)

    class Meta:
        model = Question
        fields = ['user_email', 'question']


class ClimateQuestionForm(forms.Form):
    categories = forms.MultipleChoiceField(widget=TagWidget,
                              choices=[(c.name, c.name) for c in AnswerCategory.objects.all()], required=False)
    main_question = forms.CharField(max_length=1000)
    relevant_location = forms.CharField(max_length=1000, required=False)
    relevant_timespan = forms.CharField(max_length=1000, required=False)
    extra_info = forms.CharField(max_length=5000, required=False)
    user_email = forms.EmailField()
    accept_terms = forms.BooleanField(label=_('Accept Terms & Conditions'), required=True)
