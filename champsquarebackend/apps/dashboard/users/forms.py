from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.loading import get_model

User = get_user_model()


class UserSearchForm(forms.Form):
    email = forms.CharField(required=False, label=_("Email"))
    name = forms.CharField(
        required=False, label=pgettext_lazy("User's name", "Name"))
