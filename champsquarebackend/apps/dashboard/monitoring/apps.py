from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class MonitoringDashboardConfig(AppDashboardConfig):
    label = 'monitoring_dashboard'
    name = 'champsquarebackend.apps.dashboard.monitoring'
    verbose_name = _('Monitoring Dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        #self.quiz_list_view = get_class('dashboard.quiz.views', 'QuizListView')
        pass
        
        

    def get_urls(self):
        urls = [
            path('video-room', TemplateView.as_view(template_name="champsquarebackend/dashboard/monitoring/video_room.html"), name='video-room'),
            
        ]
        return self.post_process_urls(urls)
