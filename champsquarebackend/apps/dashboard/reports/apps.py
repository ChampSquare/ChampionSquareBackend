from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class ReportsDashboardConfig(AppDashboardConfig):
    label = 'reports_dashboard'
    name = 'champsquarebackend.apps.dashboard.reports'
    verbose_name = _('Reports dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.index_view = get_class('dashboard.reports.views', 'IndexView')

    def get_urls(self):
        urls = [
            url(r'^$', self.index_view.as_view(), name='reports-index'),
        ]
        return self.post_process_urls(urls)
