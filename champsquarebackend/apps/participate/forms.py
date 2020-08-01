from django import forms
from django.utils.translation import gettext_lazy as _


try:
    # Django 3.0 and above
    from django.utils.http import url_has_allowed_host_and_scheme       # noqa F401
except ImportError:
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme

from champsquarebackend.core.loading import get_model

Participant = get_model('participate', 'Participant')


class OtpForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    otp = forms.CharField(max_length=6,
                          label='Enter 6 digit OTP',
                          help_text='To continue to test, enter the otp that was sent with with',
                          widget=forms.PasswordInput)
    

    error_messages = {
        'invalid_otp': _(
            "Either the user doesn't exist or entered otp is incorrect/expired"
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self,request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        self.participant_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        otp = self.cleaned_data.get('otp')

        if otp is not None:
            participant = Participant.objects.filter(otp_code=otp).first()
            if participant is not None:
                self.participant_cache = participant
                self.user_cache = participant.user
            else:
                raise self.get_invalid_otp_error()
            
            if self.user_cache is None:
                raise self.get_invalid_otp_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_participant(self):
        return self.participant_cache

    def get_invalid_otp_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_otp']
        )

    def clean_redirect_url(self):
        if self.participant_cache is not None:
            return self.participant_cache.get_absolute_url()
        url = self.cleaned_data['redirect_url'].strip()
        if url and url_has_allowed_host_and_scheme(url, self.host):
            return url