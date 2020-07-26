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
        self.quiz_participant_list_view = get_class('dashboard.participate.views', 'QuizParticipantListView')
        self.participant_detail_view = get_class('dashboard.participate.views', 'ParticipantDetailView')
        self.participant_create_update_view = get_class('dashboard.participate.views', 'ParticipantCreateUpdateView')

    def get_urls(self):
        urls = [
            path('quiz/<int:pk>/list/', self.quiz_participant_list_view.as_view(), name='quiz-participant-list'),
            path('<int:pk>', self.participant_detail_view.as_view(), name='participant-detail'),
            path('<int:pk>/update/quiz/<int:quiz_pk>/', self.participant_create_update_view.as_view(), name='quiz-participant-update'),
            path('create/quiz/<int:quiz_pk/', self.participant_create_update_view.as_view(), name='quiz-participant-create'),
        ]
        return self.post_process_urls(urls)
