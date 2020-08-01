from django.urls import path, reverse_lazy

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class QuizConfig(AppConfig):
    label = 'quiz'
    name = 'champsquarebackend.apps.quiz'
    verbose_name = _('Quiz')
    default_permissions = ['is_authenticated', ]
    login_url = reverse_lazy('participate:otp-login')

    namespace = 'quiz'

    def ready(self):
        self.quiz_take = get_class('quiz.views', 'QuizView')
        self.save_answer = get_class('quiz.views', 'SaveAnswer')
        self.save_unanswered = get_class('quiz.views', 'SaveUnanswered')
        self.clear_answer = get_class('quiz.views', 'ClearAnswer')
        self.answerpaper_detail = get_class('quiz.views', 'AnswerPaperDetail')
        self.save_answerpaper_status = get_class('quiz.views', 'SaveAnswerPaperStatusView')

    def get_urls(self):
        urls = [
            path('take/<int:pk>/<str:number>/', self.quiz_take.as_view(), name='quiz-take'),
            path('answerpaper/<int:pk>', self.answerpaper_detail.as_view(), name='answerpaper-detail'),
            path('error/', TemplateView.as_view(template_name="champsquarebackend/error.html"), name='error'),
            # todo : create a better and secure way to submit answers
            path('ajax/save_answer/', self.save_answer.as_view(), name='save_answer'),
            path('ajax/clear_answer/', self.clear_answer.as_view(), name='clear_answer'),
            path('ajax/save_unanswered/', self.save_unanswered.as_view(), name='save_unanswered'),
            path('ajax/save_status/', self.save_answerpaper_status.as_view(), name='save_answerpaper_status'),

            path('quiz-beta/', TemplateView.as_view(template_name="champsquarebackend/quiz/quiz_beta.html"), name='quiz-beta'),

        ]

        return self.post_process_urls(urls)
