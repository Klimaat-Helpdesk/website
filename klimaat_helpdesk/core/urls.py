from django.urls import path
from django.views.generic import TemplateView

from klimaat_helpdesk.core.views import home_page, new_question

app_name = 'core'

urlpatterns = [
    path("", view=home_page, name='home'),
    path('ask', new_question, name='ask'),
    path('ask/thanks', TemplateView.as_view(template_name='core/new_question_thanks.html'), name='new-question-thanks'),
]
