from django.urls import path
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.application import AppDashboardConfig
from champsquarebackend.core.loading import get_class


class QuizDashboardConfig(AppDashboardConfig):
    label = 'quiz_dashboard'
    name = 'champsquarebackend.apps.dashboard.quiz'
    verbose_name = _('Quiz dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.quiz_list_view = get_class('dashboard.quiz.views', 'QuizListView')
        self.quiz_create_update_view = get_class('dashboard.quiz.views', 'QuizCreateUpdateView')
        self.category_create_update_view = get_class('dashboard.quiz.views', 'CategoryCreateUpdateView')
        self.questionpaper_create_update_view = get_class('dashboard.quiz.views', 'QuestionPaperCreateUpdateView')
        self.answer_paper_detail_view = get_class('dashboard.quiz.views', 'AnswerPaperDetailView')
        self.add_user_view = get_class('dashboard.quiz.views', 'AddUserView')
        self.quiz_participant_view = get_class('dashboard.quiz.views', 'QuizParticipantView')

    def get_urls(self):
        urls = [
            path('', self.quiz_list_view.as_view(), name='quiz-list'),
            path('create/', self.quiz_create_update_view.as_view(), name='quiz-create'),
            path('<int:pk>/', self.quiz_create_update_view.as_view(), name='quiz-update'),
            path('category/new/', self.category_create_update_view.as_view(), name='quiz-category-create'),
            path('category/<int:pk>/', self.category_create_update_view.as_view(), name='quiz-category-update'),
            path('questionpaper/<int:pk>/', self.questionpaper_create_update_view.as_view(), name='quiz-questionpaper-update'),
            path('answerpaper/<int:pk>/', self.answer_paper_detail_view.as_view(), name='quiz-answerpaper-detail'),
            path('<int:pk>/users/add/', self.add_user_view.as_view(), name='quiz-add-user'),
            path('<int:pk>/participants/', self.quiz_participant_view.as_view(), name='quiz-participant-list')
        ]
        return self.post_process_urls(urls)
