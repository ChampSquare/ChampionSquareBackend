from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuizConfig(AppConfig):
    name = 'champsquarebackend.quiz'
    verbose_name = _('Quizzes')

    def ready(self):
        try: 
            import champsquarebackend.quiz.signals
        except ImportError:
            pass

