from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site

from champsquarebackend.core.loading import get_class

User = get_user_model()
UserDispatcher = get_class('user.utils', 'UserDispatcher')

class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User

class UserCreationForm(auth_forms.UserCreationForm):
    error_message = auth_forms.UserCreationForm.error_messages.update(
        {'duplicate_username': 'This username has already been taken'
    })

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            username = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        
        raise ValidationError(self.error_messages['duplicate_username'])

class PasswordResetForm(auth_forms.PasswordResetForm):
    """
        This form takes takes the same structure as its parent from :py:mod:`django.contrib.auth`
    """

    def save(self, domain_override=None, request=None, **kwargs):
        """
            Generates a one-use only link for resetting password and sends to the user
        """
        site = get_current_site(request)
        if domain_override is not None:
            site.domain = site.name = domain_override
        for user in self.get_users(self.cleaned_data['email']):
            self.send_password_reset_email(site, user)

    def send_password_reset_email(self, site, user):
        extra_context = {
            'user': user,
            'site': site,
            'reset_url': get_password_reset_url(site, user),
        }

        UserDispatcher().send_password_reset_email_for_user(user, extra_context)