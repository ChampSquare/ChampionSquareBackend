from django.forms.models import modelform_factory

from champsquarebackend.core.loading import get_model, get_class

Quiz = get_model('quiz', 'quiz')
Attribute = get_model('quiz', 'Attribute')
QuizAttributeForm = get_class('dashboard.quiz.forms', 'QuizAttributeForm')

QuizAttributeFormset = modelform_factory(
    Attribute, form=QuizAttributeForm)
