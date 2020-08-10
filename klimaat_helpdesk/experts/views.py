from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from klimaat_helpdesk.experts.models import Expert


class ExpertAnswerOverviewPage(TemplateView):
    template_name = 'experts/expert_answer_overview_page.html'

    def get_context_data(self, **kwargs):

        expert_id = kwargs.pop('id')

        if expert_id:
            expert = get_object_or_404(Expert, pk=expert_id)
            answers = expert.get_answered_questions()

            context = super(ExpertAnswerOverviewPage, self).get_context_data(**kwargs)
            context.update({
                'answers' : answers
            })
            return context

        else:
            return HttpResponseNotFound()

expert_answer_overview_page = ExpertAnswerOverviewPage.as_view()
