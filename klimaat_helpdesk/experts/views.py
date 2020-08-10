from django.views.generic import TemplateView

from klimaat_helpdesk.experts.models import Expert


class ExpertAnswerOverviewPage(TemplateView):
    template_name = 'experts/expert_answer_overview_page.html'

    def get_context_data(self, **kwargs):

        print(**kwargs)

        expert_id = 1
        if expert_id:
            expert = Expert.get_object_or_404(pk=id)
            answers = expert.get_answered_questions()

            context = super(ExpertAnswerOverviewPage, self).get_context_data(**kwargs)
            context.update({
                'answers' : []
            })
            return context

        else:
            return 'TODO HTTP 404'


expert_answer_overview_page = ExpertAnswerOverviewPage.as_view()
