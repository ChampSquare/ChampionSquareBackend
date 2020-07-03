from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class QuizConfig(AppConfig):
    label = 'quiz'
    name = 'champsquarebackend.apps.quiz'
    verbose_name = _('Quiz')

    namespace = 'quiz'

    def ready(self):
        pass

    def get_urls(self):
        urls = []

        return self.post_process_urls(urls)
