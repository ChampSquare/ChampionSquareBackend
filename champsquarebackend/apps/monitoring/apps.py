from django.urls import path

from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class MonitoringConfig(AppConfig):
    label = 'monitoring'
    name = 'champsquarebackend.apps.monitoring'
    verbose_name = _('Monitoring')
    default_permissions = ['is_authenticated', ]

    namespace = 'monitoring'

    def ready(self):
        self.save_video_record = get_class('monitoring.views', 'SaveVideoRecordView')

    def get_urls(self):
        urls = [
            path('ajax/save_video_record/', self.save_video_record.as_view(), name='video-save')    
        ]

        return self.post_process_urls(urls)
