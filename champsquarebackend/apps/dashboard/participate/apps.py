from django.urls import path
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class ParticipateDashboardConfig(AppDashboardConfig):
    label = 'participate_dashboard'
    name = 'champsquarebackend.apps.dashboard.participate'
    verbose_name = _('Participants Dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.participate_list_view = get_class('dashboard.participate.views', 'ParticipateListView')

    def get_urls(self):
        urls = [
            path('participate-list/<int:pk>', self.participate_list_view.as_view(), name='participate-list'),
        ]
        return self.post_process_urls(urls)
