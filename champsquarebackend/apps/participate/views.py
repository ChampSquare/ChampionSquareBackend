from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseBadRequest
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.loading import get_model, get_class

OtpForm = get_class('participate.forms', 'OtpForm')

class OtpAuthView(FormView):
    """
    This is actually a slightly odd double form view that allows a user to
    either login or register.
    """
    template_name = 'champsquarebackend/participate/otp_login.html'
    form_class = OtpForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # logout user first
            auth_logout(request)
            
        return super().get(
            request, *args, **kwargs)


    def form_valid(self, form):
        auth_login(self.request, form.get_user(),
                   backend='champsquarebackend.apps.user.auth_backends.EmailBackend')
        # invalidate this otp
        form.get_participant().invalidate_otp()
        return redirect(self.get_login_success_url(form))

    def get_login_success_url(self, form):
        redirect_url = form.clean_redirect_url()
        if redirect_url:
            return redirect_url