from django.urls import path
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class QuestionsDashboardConfig(AppDashboardConfig):
    label = 'questions_dashboard'
    name = 'champsquarebackend.apps.dashboard.questions'
    verbose_name = _('Questions dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.question_list_view = get_class('dashboard.questions.views', 'QuestionListView')
        self.question_create_update_view = get_class('dashboard.questions.views', 'QuestionCreateUpdateView')
        self.subject_create_update_view = get_class('dashboard.questions.subjects.views', 'SubjectCreateUpdateView')
       
        
    def get_urls(self):
        urls = [
            path('', self.question_list_view.as_view(), name='questions-list'),
            path('question-create/', self.question_create_update_view.as_view(), name='question-create'),
            path('question-update/<int:pk>/', self.question_create_update_view.as_view(), name='question-update'),
            path('question-subject-create/', self.subject_create_update_view.as_view(), name='question-subject-create'),
            path('question-subject-update/<int:pk>/', self.subject_create_update_view.as_view(), name='question-subject-update')
        ]
        return self.post_process_urls(urls)
