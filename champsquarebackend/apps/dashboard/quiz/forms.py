import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.loading import get_model
from champsquarebackend.forms import widgets

Category = get_model('quiz', 'category')
Quiz = get_model('quiz', 'quiz')
QuestionPaper = get_model('quiz', 'questionpaper')
Question = get_model('question', 'question')



class CategoryForm(forms.ModelForm):
    """
        Form to add category for quiz
    """

    class Meta:
        model = Category
        fields = ['name', 'description', 'is_public', 'image']


class QuizForm(forms.ModelForm):
    """
        Form to add quiz
    """

    class Meta:
        model = Quiz
        fields = ['name', 'description', 'category', 'instructions',
                  'start_date_time', 'end_date_time', 'duration',
                  'is_published', 'is_public', 'multiple_attempts_allowed',
                  'view_answerpaper']

class QuizMetaForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['name', 'description', 'category', 'duration']

class QuestionPaperForm(forms.ModelForm):
    """
        Form for adding questions to Quiz
    """
    class Meta:
        model = QuestionPaper
        fields = ['questions']

class QuizRestrictionsForm(forms.ModelForm):
    start_date_time = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(),
        label=_("start Date"), required=False)
    end_date_time = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(),
        label=_("End Date"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['start_date_time'].initial = today
    
    class Meta:
        model = Quiz
        fields = ['start_date_time', 'end_date_time', 'is_published', 
                    'is_public', 'multiple_attempts_allowed', 'view_answerpaper']

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data['start_date_time']
        end = cleaned_data['end_date_time']
        if start and end and end < start:
            raise forms.ValidationError(_(
                "The end date must be after the start date"))
        return cleaned_data


