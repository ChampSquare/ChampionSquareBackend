from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class OnlineTestPlatform(AppConfig):
    name = 'championsquare'

    def ready(self):
        from django.contrib.auth.forms import SetPasswordForm

        self.quiz_app = apps.get_app_config('quiz')
        self.user_app = apps.get_app_config('user')
        self.dashboard_app = apps.get_app_config('dashboard')

        self.password_reset_form = get_class('users.forms', 'PasswordResetForm')
        self.set_password_form = SetPasswordForm

    def get_urls(self):
        from django.contrib.auth import views as auth_views

        from champsquarebackend.views.decorators import login_forbidden

        urls = [
            path('', RedirectView.as_view(url=settings.HOMEPAGE_URL), name='home'),
            path('quiz/', self.quiz_app.urls),
            path('user/', self.user_app.urls),
            path('dashboard/', self.dashboard_app.urls),

            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            url(r'^password-reset/$',
                login_forbidden(
                    auth_views.PasswordResetView.as_view(
                        form_class=self.password_reset_form,
                        success_url=reverse_lazy('password-reset-done'),
                        template_name='oscar/registration/password_reset_form.html'
                    )
                ),
                name='password-reset'),
            url(r'^password-reset/done/$',
                login_forbidden(auth_views.PasswordResetDoneView.as_view(
                    template_name='oscar/registration/password_reset_done.html'
                )),
                name='password-reset-done'),
            url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                login_forbidden(
                    auth_views.PasswordResetConfirmView.as_view(
                        form_class=self.set_password_form,
                        success_url=reverse_lazy('password-reset-complete'),
                        template_name='oscar/registration/password_reset_confirm.html'
                    )
                ),
                name='password-reset-confirm'),
            url(r'^password-reset/complete/$',
                login_forbidden(auth_views.PasswordResetCompleteView.as_view(
                    template_name='oscar/registration/password_reset_complete.html'
                )),
                name='password-reset-complete'),
        ]