"""
Vanilla Quiz and related models
"""
from champsquarebackend.apps.quiz.abstract_models import * # noqa
from champsquarebackend.core.loading import is_model_registered

__all__ = []

if not is_model_registered('quiz', 'Category'):
    class Category(AbstractCategory):
        pass

    __all__.append('Category')

if not is_model_registered('quiz', 'Quiz'):
    class Quiz(AbstractQuiz):
        pass

    __all__.append('Quiz')

if not is_model_registered('quiz', 'QuestionPaper'):
    class QuestionPaper(AbstractQuestionPaper):
        pass

    __all__.append('QuestionPaper')

if not is_model_registered('quiz', 'AnswerPaper'):
    class AnswerPaper(AbstractAnswerPaper):
        pass

    __all__.append('AnswerPaper')

if not is_model_registered('quiz', 'Answer'):
    class Answer(AbstractAnswer):
        pass

    __all__.append('Answer')
