"""
Vanilla participate and related models
"""
from champsquarebackend.apps.participate.abstract_models import * # noqa
from champsquarebackend.core.loading import is_model_registered

__all__ = []

if not is_model_registered('participate', 'Participate'):
    class Participate(AbstractParticipate):
        pass

    __all__.append('Participate')