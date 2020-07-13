from django.apps import apps
from django.urls import path
from django.conf.urls import include
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
        self.questions_app = apps.get_app_config('questions_dashboard')
        self.quiz_app = apps.get_app_config('quiz_dashboard')
        self.monitoring_app = apps.get_app_config('monitoring_dashboard')


        
    def get_urls(self):
        from django.contrib.auth import views as auth_views
        from django.contrib.auth.forms import AuthenticationForm

        urls = [
            path('', self.index_view.as_view(), name='index'),
            path('users/', include(self.users_app.urls[0])),
            path('pages/', include(self.pages_app.urls[0])),
            path('comms/', include(self.comms_app.urls[0])),
            path('questions/', include(self.questions_app.urls[0])),
            path('quiz/', include(self.quiz_app.urls[0])),
            path('monitoring/', include(self.monitoring_app.urls[0])),


            
            path('login/',
                auth_views.LoginView.as_view(template_name='champsquarebackend/dashboard/login.html',
                                             authentication_form=AuthenticationForm),
                name='login'),
            path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

        ]
        return self.post_process_urls(urls)
