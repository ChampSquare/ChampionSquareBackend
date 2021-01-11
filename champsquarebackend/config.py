from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy, re_path
from django.views.generic.base import RedirectView

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class OnlineTestPlatform(AppConfig):
    name = 'champsquarebackend'

    def ready(self):
        from django.contrib.auth.forms import SetPasswordForm
        self.landing_app = apps.get_app_config('landing')
        self.user_app = apps.get_app_config('user')
        self.question_app = apps.get_app_config('question')
        self.quiz_app = apps.get_app_config('quiz')
        self.participant_app = apps.get_app_config('participate')
        self.monitoring_app = apps.get_app_config('monitoring')
        self.communication_app = apps.get_app_config('communication')

        self.password_reset_form = get_class('user.forms', 'PasswordResetForm')
        self.set_password_form = SetPasswordForm
        self.dashboard_app = apps.get_app_config('dashboard')
        


    def get_urls(self):
        from django.contrib.auth import views as auth_views

        from champsquarebackend.views.decorators import login_forbidden

        urls = [
            path('', self.landing_app.urls),
            path('user/', self.user_app.urls),
            path('dashboard/', self.dashboard_app.urls),
            path('question/', self.question_app.urls),
            path('quiz/', self.quiz_app.urls),
            path('participant/', self.participant_app.urls),
            path('monitoring/', self.monitoring_app.urls),
            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            path('password-reset/',
                login_forbidden(
                    auth_views.PasswordResetView.as_view(
                        form_class=self.password_reset_form,
                        success_url=reverse_lazy('password-reset-done'),
                        template_name='registration/password_reset_form.html'
                    )
                ),
                name='password-reset'),
            path('password-reset/done/',
                login_forbidden(auth_views.PasswordResetDoneView.as_view(
                    template_name='registration/password_reset_done.html'
                )),
                name='password-reset-done'),
            re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                login_forbidden(
                    auth_views.PasswordResetConfirmView.as_view(
                        form_class=self.set_password_form,
                        success_url=reverse_lazy('password-reset-complete'),
                        template_name='registration/password_reset_confirm.html'
                    )
                ),
                name='password-reset-confirm'),
            path('password-reset/complete/',
                login_forbidden(auth_views.PasswordResetCompleteView.as_view(
                    template_name='registration/password_reset_complete.html'
                )),
                name='password-reset-complete'),
            ]
        return urls