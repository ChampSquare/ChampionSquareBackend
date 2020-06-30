"""
Vanilla Question and related models
"""
from champsquarebackend.apps.question.abstract_models import * # noqa
from champsquarebackend.core.loading import is_model_registered

__all__ = []

if not is_model_registered('question', 'Subject'):
    class Subject(AbstractSubject):
        pass

    __all__.append['Subject']