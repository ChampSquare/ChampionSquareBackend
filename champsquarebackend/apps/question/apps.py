from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class QuestionConfig(AppConfig):
    label = 'question'
    name = 'champsquarebackend.apps.question'
    verbose_name = _('Question')

    namespace = 'question'

    def ready(self):
        pass

    def get_urls(self):
        urls = []

        return self.post_process_urls(urls)

