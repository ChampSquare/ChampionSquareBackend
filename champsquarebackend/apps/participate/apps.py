from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class ParticipateConfig(AppConfig):
    label = 'participate'
    name = 'champsquarebackend.apps.participate'
    verbose_name = _('Question')

    namespace = 'participate'

    def ready(self):
        pass

    def get_urls(self):
        urls = []

        return self.post_process_urls(urls)

