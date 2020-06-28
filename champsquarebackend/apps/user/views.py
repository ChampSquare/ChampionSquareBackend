from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from champsquarebackend.apps.user.utils import get_password_reset_url
from champsquarebackend.core.loading import (
    get_class, get_classes, get_model, get_profile_class)
from champsquarebackend.core.utils import safe_referrer
from champsquarebackend.core.compat import get_user_model


from . import signals

PageTitleMixin, RegisterUserMixin = get_classes(
    'user.mixins', ['PageTitleMixin', 'RegisterUserMixin'])
UserDispatcher = get_class('user.utils', 'UserDispatcher')
EmailAuthenticationForm, EmailUserCreationForm = get_classes(
    'user.forms', ['EmailAuthenticationForm', 'EmailUserCreationForm'])
ProfileForm, ConfirmPasswordForm = get_classes(
    'user.forms', ['ProfileForm', 'ConfirmPasswordForm'])
Email = get_model('communication', 'Email')

User = get_user_model()


# =======
# Account
# =======


class AccountSummaryView(generic.RedirectView):
    """
    View that exists for legacy reasons and customisability. It commonly gets
    called when the user clicks on "Account" in the navbar.

    Oscar defaults to just redirecting to the profile summary page (and
    that redirect can be configured via SETTINGS_ACCOUNT_REDIRECT_URL), but
    it's also likely you want to display an 'account overview' page or
    such like. The presence of this view allows just that, without
    having to change a lot of templates.
    """
    pattern_name = settings.SETTINGS_ACCOUNTS_REDIRECT_URL
    permanent = False


class AccountRegistrationView(RegisterUserMixin, generic.FormView):
    form_class = EmailUserCreationForm
    template_name = 'champsquarebackend/user/registration.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(
            request, *args, **kwargs)

    def get_logged_in_redirect(self):
        return reverse('user:summary')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'email': self.request.GET.get('email', ''),
            'redirect_url': self.request.GET.get(self.redirect_field_name, '')
        }
        kwargs['host'] = self.request.get_host()
        return kwargs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        ctx['cancel_url'] = safe_referrer(self.request, '')
        return ctx

    def form_valid(self, form):
        self.register_user(form)
        return redirect(form.cleaned_data['redirect_url'])


class AccountAuthView(RegisterUserMixin, generic.TemplateView):
    """
    This is actually a slightly odd double form view that allows a user to
    either login or register.
    """
    template_name = 'champsquarebackend/user/login_registration.html'
    login_prefix, registration_prefix = 'login', 'registration'
    login_form_class = EmailAuthenticationForm
    registration_form_class = EmailUserCreationForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(
            request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        if 'login_form' not in kwargs:
            ctx['login_form'] = self.get_login_form()
        if 'registration_form' not in kwargs:
            ctx['registration_form'] = self.get_registration_form()
        return ctx

    def post(self, request, *args, **kwargs):
        # Use the name of the submit button to determine which form to validate
        if 'login_submit' in request.POST:
            return self.validate_login_form()
        elif 'registration_submit' in request.POST:
            return self.validate_registration_form()
        return http.HttpResponseBadRequest()

    # LOGIN

    def get_login_form(self, bind_data=False):
        return self.login_form_class(
            **self.get_login_form_kwargs(bind_data))

    def get_login_form_kwargs(self, bind_data=False):
        kwargs = {}
        kwargs['request'] = self.request
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.login_prefix
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def validate_login_form(self):
        form = self.get_login_form(bind_data=True)
        if form.is_valid():
            user = form.get_user()

            # Grab a reference to the session ID before logging in
            old_session_key = self.request.session.session_key

            auth_login(self.request, form.get_user())

            # Raise signal robustly (we don't want exceptions to crash the
            # request handling). We use a custom signal as we want to track the
            # session key before calling login (which cycles the session ID).
            signals.user_logged_in.send_robust(
                sender=self, request=self.request, user=user,
                old_session_key=old_session_key)

            msg = self.get_login_success_message(form)
            if msg:
                messages.success(self.request, msg)

            return redirect(self.get_login_success_url(form))

        ctx = self.get_context_data(login_form=form)
        return self.render_to_response(ctx)

    def get_login_success_message(self, form):
        return _("Welcome back")

    def get_login_success_url(self, form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        # Redirect staff members to dashboard as that's the most likely place
        # they'll want to visit if they're logging in.
        if self.request.user.is_staff:
            return reverse('dashboard:index')

        # return settings.LOGIN_REDIRECT_URL
        return reverse('user:summary')

    # REGISTRATION

    def get_registration_form(self, bind_data=False):
        return self.registration_form_class(
            **self.get_registration_form_kwargs(bind_data))

    def get_registration_form_kwargs(self, bind_data=False):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.registration_prefix
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def validate_registration_form(self):
        form = self.get_registration_form(bind_data=True)
        if form.is_valid():
            self.register_user(form)

            msg = self.get_registration_success_message(form)
            messages.success(self.request, msg)

            return redirect(self.get_registration_success_url(form))

        ctx = self.get_context_data(registration_form=form)
        return self.render_to_response(ctx)

    def get_registration_success_message(self, form):
        return _("Thanks for registering!")

    def get_registration_success_url(self, form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        return settings.LOGIN_REDIRECT_URL


class LogoutView(generic.RedirectView):
    url = settings.SETTINGS_HOMEPAGE
    permanent = False

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super().get(request, *args, **kwargs)

        for cookie in settings.SETTINGS_COOKIES_DELETE_ON_LOGOUT:
            response.delete_cookie(cookie)

        return response


# =============
# Profile
# =============


class ProfileView(PageTitleMixin, generic.TemplateView):
    template_name = 'champsquarebackend/user/profile/profile.html'
    page_title = _('Profile')
    active_tab = 'profile'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile_fields'] = self.get_profile_fields(self.request.user)
        return ctx

    def get_profile_fields(self, user):
        field_data = []

        # Check for custom user model
        for field_name in User._meta.additional_fields:
            field_data.append(
                self.get_model_field_data(user, field_name))

        # Check for profile class
        profile_class = get_profile_class()
        if profile_class:
            try:
                profile = profile_class.objects.get(user=user)
            except ObjectDoesNotExist:
                profile = profile_class(user=user)

            field_names = [f.name for f in profile._meta.local_fields]
            for field_name in field_names:
                if field_name in ('user', 'id'):
                    continue
                field_data.append(
                    self.get_model_field_data(profile, field_name))

        return field_data

    def get_model_field_data(self, model_class, field_name):
        """
        Extract the verbose name and value for a model's field value
        """
        field = model_class._meta.get_field(field_name)
        if field.choices:
            value = getattr(model_class, 'get_%s_display' % field_name)()
        else:
            value = getattr(model_class, field_name)
        return {
            'name': getattr(field, 'verbose_name'),
            'value': value,
        }


class ProfileUpdateView(PageTitleMixin, generic.FormView):
    form_class = ProfileForm
    template_name = 'champsquarebackend/user/profile/profile_form.html'
    page_title = _('Edit Profile')
    active_tab = 'profile'
    success_url = reverse_lazy('user:profile-view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Grab current user instance before we save form.  We may need this to
        # send a warning email if the email address is changed.
        try:
            old_user = User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            old_user = None

        form.save()

        # We have to look up the email address from the form's
        # cleaned data because the object created by form.save() can
        # either be a user or profile instance depending whether a profile
        # class has been specified by the AUTH_PROFILE_MODULE setting.
        new_email = form.cleaned_data.get('email')
        if new_email and old_user and new_email != old_user.email:
            # Email address has changed - send a confirmation email to the old
            # address including a password reset link in case this is a
            # suspicious change.
            self.send_email_changed_email(old_user, new_email)

        messages.success(self.request, _("Profile updated"))
        return redirect(self.get_success_url())

    def send_email_changed_email(self, old_user, new_email):
        user = self.request.user
        extra_context = {
            'user': user,
            'reset_url': get_password_reset_url(old_user),
            'new_email': new_email,
        }
        UserDispatcher().send_email_changed_email_for_user(old_user, extra_context)


class ProfileDeleteView(PageTitleMixin, generic.FormView):
    form_class = ConfirmPasswordForm
    template_name = 'champsquarebackend/user/profile/profile_delete.html'
    page_title = _('Delete profile')
    active_tab = 'profile'
    success_url = settings.SETTINGS_HOMEPAGE

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.request.user.delete()
        messages.success(
            self.request,
            _("Your profile has now been deleted. Thanks for using the site."))
        return redirect(self.get_success_url())


class ChangePasswordView(PageTitleMixin, generic.FormView):
    form_class = PasswordChangeForm
    template_name = 'champsquarebackend/user/profile/change_password_form.html'
    page_title = _('Change Password')
    active_tab = 'profile'
    success_url = reverse_lazy('user:profile-view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, _("Password updated"))

        self.send_password_changed_email()

        return redirect(self.get_success_url())

    def send_password_changed_email(self):
        user = self.request.user
        extra_context = {
            'user': user,
            'reset_url': get_password_reset_url(self.request.user),
        }
        UserDispatcher().send_password_changed_email_for_user(user, extra_context)


# =============
# Email history
# =============

class EmailHistoryView(PageTitleMixin, generic.ListView):
    context_object_name = "emails"
    template_name = 'champsquarebackend/communication/email/email_list.html'
    paginate_by = settings.SETTINGS_EMAILS_PER_PAGE
    page_title = _('Email History')
    active_tab = 'emails'

    def get_queryset(self):
        """
        Return Queryset of :py:class:`Email <champsquarebackend.apps.user.abstract_models.AbstractEmail>`
        instances, that has been sent to the currently authenticated user.
        """  # noqa
        return Email._default_manager.filter(user=self.request.user)


class EmailDetailView(PageTitleMixin, generic.DetailView):
    """Customer email"""
    template_name = "champsquarebackend/communication/email/email_detail.html"
    context_object_name = 'email'
    active_tab = 'emails'

    def get_object(self, queryset=None):
        return get_object_or_404(Email, user=self.request.user,
                                 id=self.kwargs['email_id'])

    def get_page_title(self):
        """Append email subject to page title"""
        return '%s: %s' % (_('Email'), self.object.subject)