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
        self.quiz_metadata_create_update_view = get_class('dashboard.quiz.views', 'QuizMetaDataCreateUpdateView')
        self.quiz_questionpaper_create_update_view = get_class('dashboard.quiz.views', 'QuizQuestionPaperCreateUpdateView')
        self.quiz_restrictions_create_update_view = get_class('dashboard.quiz.views', 'QuizRestrictionsCreateUpdateView')
        self.questionpaper_create_update_view = get_class('dashboard.quiz.views', 'QuestionPaperCreateUpdateView')
        

    def get_urls(self):
        urls = [
            path('', self.quiz_list_view.as_view(), name='quiz-list'),
            path('quiz-create/', self.quiz_create_update_view.as_view(), name='quiz-create'),
            path('quiz-update/<int:pk>/', self.quiz_create_update_view.as_view(), name='quiz-update'),
            path('quiz-category-create/', self.category_create_update_view.as_view(), name='quiz-category-create'),
            path('quiz-category-update/<int:pk>/', self.category_create_update_view.as_view(), name='quiz-category-update'),
            path('questionpaper-create/<int:pk>/', self.questionpaper_create_update_view.as_view(), name='quiz-questionpaper-update'),

            #creation
            path('new/name-and-description/', self.quiz_metadata_create_update_view.as_view(),
                name='quiz-metadata'),
            path('new/questionpaper/', self.quiz_questionpaper_create_update_view.as_view(),
                name='quiz-questionpaper'),
            path('new/restrictions/', self.quiz_restrictions_create_update_view.as_view(),
                name='quiz-restrictions'),

            # Update
            path('<int:pk>/name-and-description/',
                self.quiz_metadata_create_update_view.as_view(update=True),
                name='quiz-metadata'),
            path('<int:pk>/questionpaper/',
                self.quiz_questionpaper_create_update_view.as_view(update=True),
                name='quiz-questionpaper'),
            path('<int:pk>/restrictions/',
                self.quiz_restrictions_create_update_view.as_view(update=True),
                name='quiz-restrictions'),
        ]
        return self.post_process_urls(urls)
