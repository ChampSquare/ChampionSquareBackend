from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'champsquarebackend.home'
    verbose_name = _("Homes")

    def ready(self):
        try:
            import champsquarebackend.home.signals
        except ImportError:
            pass

