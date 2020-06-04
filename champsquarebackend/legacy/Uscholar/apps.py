from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig


class UscholarConfig(AppConfig):
    name = 'champsquarebackend.legacy.Uscholar'
    verbose_name = _('Uscholar')

    def ready(self):
        try:
            import champsquarebackend.legacy.Uscholar.signal
        except ImportError:
            pass

