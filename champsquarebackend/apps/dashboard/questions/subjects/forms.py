from django import forms

from champsquarebackend.core.loading import get_model

Subject = get_model('question', 'subject')
Topic = get_model('question', 'topic')


class SubjectForm(forms.ModelForm):
    """
        creates a form to add subject
    """

    class Meta:
        model = Subject
        exclude = []

class TopicForm(forms.ModelForm):
    """
        creates a form to add topic
    """

    class Meta:
        model = Topic
        exclude = []
