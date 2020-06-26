from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = 'champsquarebackend.users'
    verbose_name = _("Users")

    def ready(self):
        try:
            import champsquarebackend.users.signals
        except ImportError:
            pass
