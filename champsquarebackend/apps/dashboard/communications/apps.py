from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class CommunicationsDashboardConfig(AppDashboardConfig):
    label = 'communications_dashboard'
    name = 'champsquarebackend.apps.dashboard.communications'
    verbose_name = _('Communications dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.list_view = get_class('dashboard.communications.views', 'ListView')
        self.update_view = get_class('dashboard.communications.views', 'UpdateView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='comms-list'),
            url(r'^(?P<slug>\w+)/$', self.update_view.as_view(),
                name='comms-update'),
        ]
        return self.post_process_urls(urls)
