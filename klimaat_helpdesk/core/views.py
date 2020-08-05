from random import random

from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from klimaat_helpdesk.cms.models import Answer, AnswerCategory, AnswerIndexPage, ExpertIndexPage
from klimaat_helpdesk.core.forms import AskQuestion, ClimateQuestionForm
from klimaat_helpdesk.core.models import Question
from klimaat_helpdesk.experts.models import Expert


class HomePage(TemplateView):
    template_name = 'core/home_page.html'

    def get_context_data(self, **kwargs):
        featured_answers = Answer.objects.live().filter(featured=True)[:10]
        categories = AnswerCategory.objects.all()
        featured_experts = Expert.objects.filter(featured=True)[:3]

        context = super(HomePage, self).get_context_data(**kwargs)
        context.update({
            'answers_page': AnswerIndexPage.objects.first().url,
            'experts_page': ExpertIndexPage.objects.first(),
            'featured_answers': featured_answers,
            'categories': categories,
            'featured_experts' : featured_experts
        })
        return context


home_page = HomePage.as_view()


class AskAQuestionPage(TemplateView):
    """
    This is the page where users can submit a new question. It consists of a form
    that is spread over two steps using JavaScript.
    """
    template_name = 'core/ask_a_question_page.html'

    def get_form(self):
        return ClimateQuestionForm()

    def get_random_category_and_questions(self):
        """
        We can use order by ? since its only 9 items.
        Suggested category with answers.
        """
        category = AnswerCategory.objects.order_by("?").first()
        answers = Answer.objects.live().specific().filter(category=category)[:3]

        return {
            'category' : category,
            'answers' : answers,
        }

    def get_context_data(self, **kwargs):
        context = super(AskAQuestionPage, self).get_context_data(**kwargs)
        context.update({
            'form': self.get_form(),
            'suggestion': self.get_random_category_and_questions()
        })
        return context


ask_a_question_page = AskAQuestionPage.as_view()


class NewQuestion(FormView):
    form_class = ClimateQuestionForm
    template_name = 'core/new_question.html'
    success_url = reverse_lazy('core:new-question-thanks')

    def form_valid(self, form):
        Question.objects.create(
            question=form.cleaned_data['main_question'],
            user_email=form.cleaned_data.get('user_email', None),
            asked_by_ip=self.request.META.get('REMOTE_ADDR')
        )
        return super(NewQuestion, self).form_valid(form)


new_question = NewQuestion.as_view()
