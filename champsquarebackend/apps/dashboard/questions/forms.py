from django import forms
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.loading import get_model

Question = get_model('question', 'question')



class QuestionForm(forms.ModelForm):
    """
        creates a form to add or edit a Question.
    """

    class Meta:
        model = Question
        fields = ['description', 'subject', 'topic',
                  'question_type', 'right_answer', 'points', 'negative_points',
                  'difficulty_level', 'solution']


