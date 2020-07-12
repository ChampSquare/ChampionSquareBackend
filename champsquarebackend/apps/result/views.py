from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from champsquarebackend.core.loading import get_model, get_class

Answer = get_model('quiz', 'Answer')
Participant = get_model('participant', 'Participant')


class AnswerPaperView(ListView):
    model = Answer
    context_object_name = "answers"
    template_name = 'champsquarebackend/result/detail.html'

    def get_participant(self):
        if not hasattr(self, '_participant'):
            self._participant = get_object_or_404(Participant, id=self.kwargs['pk'])
        return self._participant

    def get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = self.get_participant().quiz
        return self._quiz

    def get_answerpaper(self):
        if not hasattr(self, '_answerpaper'):
            self._answerpaper = self.get_participant().answerpaper
        return self._answerpaper

    def get_questionpaper(self):
        if not hasattr(self, '_questionpaper'):
            self._questionpaper = self.get_quiz().questionpaper
        return self._questionpaper

    def get_queryset(self):
        return self.get_quiz().questionpaper.get_all_questions()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        quiz = self.get_quiz()
        ctx['quiz'] = quiz
        ctx['participant'] = self.get_participant()
        return ctx