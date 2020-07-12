from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class QuizConfig(AppConfig):
    label = 'result'
    name = 'champsquarebackend.apps.result'
    verbose_name = _('Result')
    default_permissions = ['is_authenticated', ]

    namespace = 'result'

    def ready(self):
        pass

    def get_urls(self):
        urls = [
            
        ]

        return self.post_process_urls(urls)
