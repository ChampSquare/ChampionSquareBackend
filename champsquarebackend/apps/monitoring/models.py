"""
Vanilla Quiz and related models
"""
from champsquarebackend.apps.monitoring.abstract_models import * # noqa
from champsquarebackend.core.loading import is_model_registered

__all__ = []

if not is_model_registered('videorecord', 'Monitoring'):
    class VideoRecord(AbstractVideoRecord):
        pass

    __all__.append('VideoRecord')