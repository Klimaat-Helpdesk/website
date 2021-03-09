from django.urls import path
from django.views.generic import TemplateView

from klimaat_helpdesk.core.views import home_page, ask_a_question_page, post_question_submit_page, questions_in_progress

app_name = 'core'

urlpatterns = [
    path("", view=home_page, name='home'),
    path("in_behandeling", view=questions_in_progress, name='questions-in-progress'),
    path('ask', view=ask_a_question_page, name='ask'),
    path('ask/question_received', view=post_question_submit_page, name='post-question'),
    path('ask/thanks', TemplateView.as_view(template_name='core/new_question_thanks.html'), name='new-question-thanks'),
]
