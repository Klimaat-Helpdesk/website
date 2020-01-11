from django.views.generic import TemplateView

from klimaat_helpdesk.cms.models import Answer, AnswerCategory


class HomePage(TemplateView):
    template_name = 'core/home_page.html'

    def get_context_data(self, **kwargs):
        latest_answers = Answer.objects.live()[:10]
        categories = AnswerCategory.objects.all()
        expert_profile = None
        context = super(HomePage, self).get_context_data(**kwargs)
        context.update({
            'latest_questions': latest_answers,
            'categories': categories,
            'expert_profile': expert_profile,
        })
        return context


home_page = HomePage.as_view()
