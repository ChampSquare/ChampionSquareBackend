from django import forms
from django.utils.translation import gettext_lazy as _

from champsquarebackend.quiz.models import Question, Subject, Topic, QUESTION_TYPES

class QuestionTypeSelectionForm(forms.Form):
    """
        form which is used before creating question to select question type
    """
    question_type = forms.ChoiceField(label=_("Create a new question of type"), 
                                      choices=QUESTION_TYPES, required=True)


class AddQuestionForm(forms.ModelForm):
    """
        creates a form to add or edit a Question.
    """

    class Meta:
        model = Question
        fields = ['description', 'subject', 'topic', 
                  'question_type', 'answer_options', 'points', 'negative_points',
                  'difficulty_level', 'solution']

class AddSubjectForm(forms.ModelForm):
    """
        creates a form to add subject
    """

    class Meta:
        model = Subject
        exclude = []

class AddTopicForm(forms.ModelForm):
    """
        creates a form to add topic
    """

    class Meta:
        model = Topic
        exclude = []
