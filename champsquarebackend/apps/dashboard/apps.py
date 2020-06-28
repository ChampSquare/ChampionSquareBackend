from django.apps import apps
from django.conf.urls import include, url
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class DashboardConfig(AppDashboardConfig):
    label = 'dashboard'
    name = 'champsquarebackend.apps.dashboard'
    verbose_name = _('Dashboard')

    namespace = 'dashboard'
    permissions_map = {
        'index': (['is_staff'], ['partner.dashboard_access']),
    }

    def ready(self):
        self.index_view = get_class('dashboard.views', 'IndexView')

        # self.reports_app = apps.get_app_config('reports_dashboard')
        self.users_app = apps.get_app_config('users_dashboard')
        self.pages_app = apps.get_app_config('pages_dashboard')
        self.comms_app = apps.get_app_config('communications_dashboard')
        
    def get_urls(self):
        from django.contrib.auth import views as auth_views
        from django.contrib.auth.forms import AuthenticationForm

        urls = [
            url(r'^$', self.index_view.as_view(), name='index'),
            url(r'^users/', include(self.users_app.urls[0])),
            url(r'^pages/', include(self.pages_app.urls[0])),
            url(r'^comms/', include(self.comms_app.urls[0])),
            
            url(r'^login/$',
                auth_views.LoginView.as_view(template_name='champsquarebackend/dashboard/login.html',
                                             authentication_form=AuthenticationForm),
                name='login'),
            url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

        ]
        return self.post_process_urls(urls)
