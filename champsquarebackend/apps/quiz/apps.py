from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class QuizConfig(AppConfig):
    label = 'quiz'
    name = 'champsquarebackend.apps.quiz'
    verbose_name = _('Quiz')
    default_permissions = ['is_authenticated', ]

    namespace = 'quiz'

    def ready(self):
        self.quiz_take = get_class('quiz.views', 'QuizView')

    def get_urls(self):
        urls = [
            path('quiz-take/<int:pk>', self.quiz_take.as_view(), name='quiz-take'),
        ]

        return self.post_process_urls(urls)
