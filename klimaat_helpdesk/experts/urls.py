from django.urls import path

from klimaat_helpdesk.experts.views import expert_answer_overview_page
app_name = 'experts'

urlpatterns = [
    path('expert_answers/<int:id>/', view=expert_answer_overview_page, name='expert_answer_overview'),
]
