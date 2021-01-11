from django.urls import path
from django.contrib.auth.decorators import login_required

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class LandingConfig(AppConfig):
    label = 'landing'
    name = 'champsquarebackend.apps.landing'
    verbose_name = _('landing')

    namespace = 'landing'

    def ready(self):
        pass

    def get_urls(self):
        urls = [
            path('', TemplateView.as_view(template_name='landing/home.html'), name='home'),
            path('courses/', TemplateView.as_view(template_name="landing/courses-grid-sidebar.html"), name='courses'),
            path('course-detail/', TemplateView.as_view(template_name="landing/course-detail.html"), name='course-detail'),
            path('enroll-sample/', TemplateView.as_view(template_name="landing/enroll.html"), name='enroll'),
            path('teacher/', TemplateView.as_view(template_name="landing/teacher.html"), name='teacher')
            ]

        return self.post_process_urls(urls)

