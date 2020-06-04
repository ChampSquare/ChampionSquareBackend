from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    name = 'champsquarebackend.dashboard'
    verbose_name = _("Dashboard")

    def ready(self):
        try:
            import champsquarebackend.dashboard.signals
        except ImportError:
            pass
