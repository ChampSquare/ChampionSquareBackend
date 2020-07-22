from django import forms

from champsquarebackend.core.compat import existing_user_fields, get_user_model
from champsquarebackend.core.loading import get_class, get_model

Participate = get_model('participate', 'participate')
EmailUserCreationForm = get_class('user.forms', 'EmailUserCreationForm')

User = get_user_model()

class NewUserForm(EmailUserCreationForm):

    def __init__(self, quiz, *args, **kwargs):
        self.quiz = quiz
        super().__init__(host=None, *args, **kwargs)

    def save(self):
        user = super().save()  
        self.quiz.users.add(user)
        return user

    class Meta:
        model = User
        fields = existing_user_fields(
            ['first_name', 'last_name', 'email', 'is_staff']) + ['password1', 'password2']