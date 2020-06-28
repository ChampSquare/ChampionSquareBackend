from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class UsersDashboardConfig(AppDashboardConfig):
    label = 'users_dashboard'
    name = 'champsquarebackend.apps.dashboard.users'
    verbose_name = _('Users dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.index_view = get_class('dashboard.users.views', 'IndexView')
        self.user_detail_view = get_class('dashboard.users.views', 'UserDetailView')
        self.password_reset_view = get_class('dashboard.users.views',
                                             'PasswordResetView')
        
    def get_urls(self):
        urls = [
            url(r'^$', self.index_view.as_view(), name='users-index'),
            url(r'^(?P<pk>-?\d+)/$',
                self.user_detail_view.as_view(), name='user-detail'),
            url(r'^(?P<pk>-?\d+)/password-reset/$',
                self.password_reset_view.as_view(),
                name='user-password-reset'),
        ]
        return self.post_process_urls(urls)
