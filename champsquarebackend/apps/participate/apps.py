from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class ParticipateConfig(AppConfig):
    label = 'participate'
    name = 'champsquarebackend.apps.participate'
    verbose_name = _('Participate')

    namespace = 'participate'

    def ready(self):
        self.otp_login_view = get_class('participate.views', 'OtpAuthView')

    def get_urls(self):
        urls = [
            path('otp/login/', self.otp_login_view.as_view(), name='otp-login')
        ]

        return self.post_process_urls(urls)

