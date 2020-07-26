import string

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string

try:
    # Django 3.0 and above
    from django.utils.http import url_has_allowed_host_and_scheme       # noqa F401
except ImportError:
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme

from champsquarebackend.core.loading import get_profile_class, get_class, get_model
from champsquarebackend.apps.user.utils import get_password_reset_url, normalise_email
from champsquarebackend.core.compat import url_has_allowed_host_and_scheme, get_user_model

UserDispatcher = get_class('user.utils', 'UserDispatcher')
CommunicationEventType = get_model('communication', 'communicationeventtype')
User = get_user_model()


def generate_username():
    letters = string.ascii_letters
    allowed_chars = letters + string.digits + '_'
    uname = get_random_string(length=30, allowed_chars=allowed_chars)
    try:
        User.objects.get(username=uname)
        return generate_username()
    except User.DoesNotExist:
        return uname


class UserForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['instance'] = user
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].required = True

    def clean_email(self):
        """
        Make sure that the email address is always unique as it is
        used instead of the username. This is necessary because the
        uniqueness of email addresses is *not* enforced on the model
        level in ``django.contrib.auth.models.User``.
        """
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(
                email__iexact=email).exclude(id=self.user.id).exists():
            raise ValidationError(
                _("A user with this email address already exists"))
        # Save the email unaltered
        return email

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PasswordResetForm(auth_forms.PasswordResetForm):
    """
        This form takes takes the same structure as its parent from :py:mod:`django.contrib.auth`
    """
    communication_type_code = "PASSWORD_RESET"

    def save(self, domain_override=None, use_https=False, request=None, **kwargs):
        """
            Generates a one-use only link for resetting password and sends to the user
        """
        site = get_current_site(request)
        if domain_override is not None:
            site.domain = site.name = domain_override
        email = self.cleaned_data['email']
        active_users = User.objects.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            reset_url = self.get_reset_url(site, request, user, use_https)
            ctx = {
                'user': user,
                'site': site,
                'reset_url': reset_url}
            UserDispatcher().send_password_reset_email_for_user(user, ctx)
        
    def get_reset_url(self, site, request, user, use_https):
        # the request argument isn't used currently, but implementors might
        # need it to determine the correct subdomain
        reset_url = "%s://%s%s" % (
            'https' if use_https else 'http',
            site.domain,
            get_password_reset_url(user))

        return reset_url


class EmailAuthenticationForm(AuthenticationForm):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames. 75 character usernames are needed to support the EmailOrUsername
    authentication backend.
    """
    username = forms.EmailField(label=_('Email address'))
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and url_has_allowed_host_and_scheme(url, self.host):
            return url


class ConfirmPasswordForm(forms.Form):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames. 75 character usernames are needed to support the EmailOrUsername
    authentication backend.
    """
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError(
                _("The entered password is not valid!"))
        return password


class EmailUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email address'))
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Confirm password'), widget=forms.PasswordInput)
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, host=None, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        # Validate after self.instance is updated with form data
        # otherwise validators can't access email
        # see django.contrib.auth.forms.UserCreationForm
        if password:
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def clean_email(self):
        """
        Checks for existing users with the supplied email address.
        """
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("A user with that email address already exists"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and url_has_allowed_host_and_scheme(url, self.host):
            return url
        return settings.LOGIN_REDIRECT_URL

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if 'username' in [f.name for f in User._meta.fields]:
            user.username = generate_username()
        if commit:
            user.save()
        return user

Profile = get_profile_class()
if Profile:  # noqa (too complex (12))

    class UserAndProfileForm(forms.ModelForm):

        def __init__(self, user, *args, **kwargs):
            try:
                instance = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                # User has no profile, try a blank one
                instance = Profile(user=user)
            kwargs['instance'] = instance

            super().__init__(*args, **kwargs)

            # Get profile field names to help with ordering later
            profile_field_names = list(self.fields.keys())

            # Get user field names (we look for core user fields first)
            core_field_names = set([f.name for f in User._meta.fields])
            user_field_names = ['email']
            for field_name in ('first_name', 'last_name'):
                if field_name in core_field_names:
                    user_field_names.append(field_name)
            user_field_names.extend(User._meta.additional_fields)

            # Store user fields so we know what to save later
            self.user_field_names = user_field_names

            # Add additional user form fields
            additional_fields = forms.fields_for_model(
                User, fields=user_field_names)
            self.fields.update(additional_fields)

            # Ensure email is required and initialised correctly
            self.fields['email'].required = True

            # Set initial values
            for field_name in user_field_names:
                self.fields[field_name].initial = getattr(user, field_name)

            # Ensure order of fields is email, user fields then profile fields
            self.fields.keyOrder = user_field_names + profile_field_names

        class Meta:
            model = Profile
            exclude = ('user',)

        def clean_email(self):
            email = normalise_email(self.cleaned_data['email'])

            users_with_email = User._default_manager.filter(
                email__iexact=email).exclude(id=self.instance.user.id)
            if users_with_email.exists():
                raise ValidationError(
                    _("A user with this email address already exists"))
            return email

        def save(self, *args, **kwargs):
            user = self.instance.user

            # Save user also
            for field_name in self.user_field_names:
                setattr(user, field_name, self.cleaned_data[field_name])
            user.save()

            return super().save(*args, **kwargs)

    ProfileForm = UserAndProfileForm
else:
    ProfileForm = UserForm
