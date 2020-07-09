from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from champsquarebackend.core.loading import get_model, get_class

Question = get_model('question', 'question')
Quiz = get_model('quiz', 'quiz')
ParticipantCreator = get_class('participate.utils', 'ParticipantCreator')

class QuizView(ListView):
    """
        view to take quiz
    """
    model = Question
    context_object_name = "questions"
    template_name = 'champsquarebackend/quiz/quiz_take_admin.html'

    def get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = get_object_or_404(Quiz, id=self.kwargs['pk'])
        return self._quiz

    def get_participant(self):
        if not hasattr(self, '_participant'):
            creator = ParticipantCreator()
            self._participant = creator.start_quiz(quiz=self.get_quiz(),
                                                   request=self.request,
                                                   user=self.request.user)
        return self._participant


    def get_queryset(self):
        return self.get_quiz().questionpaper.get_all_questions()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        quiz = self.get_quiz()
        ctx['quiz'] = quiz
        ctx['participant'] = self.get_participant()
        return ctx

