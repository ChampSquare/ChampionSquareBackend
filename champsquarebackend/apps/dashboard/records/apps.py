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
        self.video_list = get_class('dashboard.records.views', 'VideoListView')
        self.video_delete_view = get_class('dashboard.records.views', 'VideoDeleteView')
        self.video_post_process_view = get_class('dashboard.records.views', 'ProcessVideoView')
        self.video_process_view = get_class('dashboard.records.views', 'TaskView')
    def get_urls(self):
        urls = [
            path('videos', TemplateView.as_view(template_name="champsquarebackend/dashboard/records/videos.html"), name='videos'),
            path('video-list', self.video_list.as_view(), name='video-list'),
            path('video/<int:pk>/delete', self.video_delete_view.as_view(), name='video-delete'),
            path('video/<int:pk>/post-process', self.video_post_process_view.as_view(), name='video-post-process'),
            path('video/<str:task_id>/', self.video_process_view.as_view(), name='process-video-task'),
        ]
        return self.post_process_urls(urls)
