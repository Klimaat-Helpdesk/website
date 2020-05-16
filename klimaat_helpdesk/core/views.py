from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from klimaat_helpdesk.cms.models import Answer, AnswerCategory, AnswerIndexPage, ExpertIndexPage
from klimaat_helpdesk.core.forms import AskQuestion
from klimaat_helpdesk.core.models import Question
from klimaat_helpdesk.experts.models import Expert


class HomePage(TemplateView):
    template_name = 'core/home_page.html'

    def get_context_data(self, **kwargs):
        latest_answers = Answer.objects.live()[:10]
        categories = AnswerCategory.objects.all()
        expert_profile = Expert.objects.first()
        context = super(HomePage, self).get_context_data(**kwargs)
        context.update({
            'answers_page': AnswerIndexPage.objects.first().url,
            'experts_page': ExpertIndexPage.objects.first(),
            'answers': latest_answers,
            'categories': categories,
            'expert_profile': expert_profile,
        })
        return context


home_page = HomePage.as_view()


class NewQuestion(FormView):
    form_class = AskQuestion
    template_name = 'core/new_question.html'
    success_url = reverse_lazy('core:new-question-thanks')

    def form_valid(self, form):
        Question.objects.create(
            question=form.cleaned_data['question'],
            user_email=form.cleaned_data.get('user_email', None),
            asked_by_ip=self.request.META.get('REMOTE_ADDR')
        )
        return super(NewQuestion, self).form_valid(form)


new_question = NewQuestion.as_view()
