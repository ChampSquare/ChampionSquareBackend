"""
Vanilla Quiz and related models
"""
from champsquarebackend.apps.result.abstract_models import * # noqa
from champsquarebackend.core.loading import is_model_registered

__all__ = []

if not is_model_registered('result', 'Result'):
    class Result(AbstractResult):
        pass

    __all__.append('Result')