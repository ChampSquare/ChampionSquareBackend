"""
Vanilla participate and related models
"""
from champsquarebackend.apps.participate.abstract_models import * # noqa
from champsquarebackend.core.loading import is_model_registered

__all__ = []

if not is_model_registered('participate', 'Participant'):
    class Participant(AbstractParticipant):
        pass

    __all__.append('Participant')