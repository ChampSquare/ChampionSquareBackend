from django.urls import path, re_path

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from champsquarebackend.core.application import AppConfig
from champsquarebackend.core.loading import get_class

class QuizConfig(AppConfig):
    label = 'quiz'
    name = 'champsquarebackend.apps.quiz'
    verbose_name = _('Quiz')
    default_permissions = ['is_authenticated', ]

    namespace = 'quiz'

    def ready(self):
        self.quiz_take = get_class('quiz.views', 'QuizView')
        self.quiz_take_monitoring = get_class('quiz.views', 'QuizWithVideoMonitoringView')
        self.save_answer = get_class('quiz.views', 'SaveAnswer')
        self.save_unanswered = get_class('quiz.views', 'SaveUnanswered')
        self.clear_answer = get_class('quiz.views', 'ClearAnswer')
        self.answerpaper_detail = get_class('quiz.views', 'AnswerPaperDetail')

    def get_urls(self):
        urls = [
            path('take/<int:pk>/<int:participant_pk>/', self.quiz_take.as_view(), name='quiz-take'),
            path('take-video/<int:pk>/<str:number>/', self.quiz_take_monitoring.as_view(), name='quiz-take-monitoring'),
            path('answerpaper/<int:pk>', self.answerpaper_detail.as_view(), name='answerpaper-detail'),
            path('error/', TemplateView.as_view(template_name="champsquarebackend/error.html"), name='error'),

            
            # todo : create a better and secure way to submit answers
            path('ajax/save_answer/', self.save_answer.as_view(), name='save_answer'),
            path('ajax/clear_answer/', self.clear_answer.as_view(), name='clear_answer'),
            path('ajax/save_unanswered/', self.save_unanswered.as_view(), name='save_unanswered'),
            # path('ajax/save_video_record/', views.save_video_record, name='save_video_record')
        ]

        return self.post_process_urls(urls)
