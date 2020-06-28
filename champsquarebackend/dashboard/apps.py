from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    name = 'champsquarebackend.apps.dashboard'
    verbose_name = _("Dashboard")

    def ready(self):
        try:
            import champsquarebackend.apps.dashboard.signals
        except ImportError:
            pass
