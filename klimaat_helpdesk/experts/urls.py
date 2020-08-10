from django.urls import path
from django.views.generic import TemplateView

from klimaat_helpdesk.experts.views import expert_answer_overview_page
app_name = 'experts'

urlpatterns = [
    path('expert_answers', view=expert_answer_overview_page, name='expert_answer_overview'),
]
