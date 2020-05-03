from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class HomeConfig(AppConfig):
    name = 'champsquarebackend.home'
    verbose_name = _("Homes")

    def ready(self):
        try:
            import champsquarebackend.home.signals
        except ImportError:
            pass

