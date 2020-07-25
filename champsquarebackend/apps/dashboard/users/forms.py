from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from champsquarebackend.core.compat import get_user_model, existing_user_fields
from champsquarebackend.core.loading import get_model, get_class

User = get_user_model()
EmailUserCreationForm = get_class('user.forms', 'EmailUserCreationForm')



class UserSearchForm(forms.Form):
    email = forms.CharField(required=False, label=_("Email"))
    name = forms.CharField(
        required=False, label=pgettext_lazy("User's name", "Name"))


class UserForm(EmailUserCreationForm):
    class Meta:
        model = User
        fields = existing_user_fields(
            ['first_name', 'last_name', 'email', 'is_staff']) + ['password1', 'password2']
