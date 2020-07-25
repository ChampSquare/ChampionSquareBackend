from django.urls import path
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class ParticipateDashboardConfig(AppDashboardConfig):
    label = 'participate_dashboard'
    name = 'champsquarebackend.apps.dashboard.participate'
    verbose_name = _('Participants Dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.participant_list_view = get_class('dashboard.participate.views', 'ParticipantListView')
        self.participant_create_view = get_class('dashboard.participate.views', 'QuizParticipantCreateView')
        self.quiz_participant_list_view = get_class('dashboard.participate.views', 'QuizParticipantListView')
        self.participant_detail_view = get_class('dashboard.participate.views', 'ParticipantDetailView')

    def get_urls(self):
        urls = [
            path('<int:pk>/new/participant/', self.participant_create_view.as_view(), name='quiz-participant-create'),
            path('participant-list/<int:pk>', self.participant_list_view.as_view(), name='participant-list'),
            path('quiz/<int:pk>/list/', self.quiz_participant_list_view.as_view(), name='quiz-participant-list'),
            path('<int:pk>', self.participant_detail_view.as_view(), name='participant-detail')
        ]
        return self.post_process_urls(urls)
