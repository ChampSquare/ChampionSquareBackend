from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class RecordsDashboardConfig(AppDashboardConfig):
    label = 'records_dashboard'
    name = 'champsquarebackend.apps.dashboard.records'
    verbose_name = _('Record Dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        pass
        
        

    def get_urls(self):
        urls = [
            path('videos', TemplateView.as_view(template_name="champsquarebackend/dashboard/records/videos.html"), name='videos'),
            
        ]
        return self.post_process_urls(urls)
