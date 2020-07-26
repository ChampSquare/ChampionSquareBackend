from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from champsquarebackend.core.loading import get_model, get_class

Question = get_model('question', 'question')
Quiz = get_model('quiz', 'quiz')
AnswerPaper = get_model('quiz', 'AnswerPaper')
Participant = get_model('participate', 'participant')
ParticipantCreator = get_class('participate.utils', 'ParticipantCreator')
QuizConditionsMixin = get_class('quiz.mixins', 'QuizConditionsMixin')

class QuizView(QuizConditionsMixin, ListView):
    """
        view to take quiz
    """
    model = Question
    context_object_name = "questions"
    template_name = 'champsquarebackend/quiz/quiz_take_admin.html'
    pre_conditions = ['is_participant',]
    skip_conditions = []

    def get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = get_object_or_404(Quiz, id=self.kwargs['pk'])
        return self._quiz

    def get_participant(self):
        if not hasattr(self, '_participant'):
            self._participant = get_object_or_404(Participant, id=self.kwargs['participant_pk'])
        return self._participant

    def get_answerpaper(self):
        if not hasattr(self, '_answerpaper'):
            creator = ParticipantCreator()
            self._answerpaper = creator.start_quiz(quiz=self.get_quiz(),
                                                   participant=self.get_participant(),
                                                   request=self.request)
        return self._answerpaper


    def get_queryset(self):
        return self.get_quiz().questionpaper.get_all_questions()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        quiz = self.get_quiz()
        ctx['quiz'] = self.get_quiz()
        ctx['participant'] = self.get_participant()
        ctx['answerpaper'] = self.get_answerpaper()
        return ctx

class QuizWithVideoMonitoringView(QuizView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['video_monitoring'] = True
        return ctx


# Legacy code
# todo: remove these and find better way to add answers


class SaveAnswer(DetailView):
    """A base view for displaying a single object."""
    def get(self, request, *args, **kwargs):
        answer_paper_id = int(request.GET.get('answer_paper_id', None))
        q_id = int(request.GET.get('question_id'))
        answer_key = request.GET.get('answer_key')
        status = request.GET.get('status')
        time_taken = request.GET.get('time_taken')

        paper = AnswerPaper.objects.get(id=answer_paper_id)
        paper.add_answer_key(q_id, answer_key, status, time_taken)
        data = {
            'success': True
        }

        return JsonResponse(data)

class ClearAnswer(DetailView):
    def get(self, request, *args, **kwargs):
        answer_paper_id = int(request.GET.get('answer_paper_id', None))
        q_id = int(request.GET.get('question_id'))
        time_taken = request.GET.get('time_taken')
        paper = AnswerPaper.objects.get(id=answer_paper_id)
        paper.clear_answer(q_id, time_taken=time_taken)
        data = {
            'success': True
        }

        return JsonResponse(data)

class SaveUnanswered(DetailView):
    def get(self, request, *args, **kwargs):
        answer_paper_id = int(request.GET.get('answer_paper_id', None))
        q_id = int(request.GET.get('question_id'))
        time_taken = request.GET.get('time_taken')
        paper = AnswerPaper.objects.get(id=answer_paper_id)
        paper.save_unanswered(q_id, time_taken)
        data = {
            'success': True
        }

        return JsonResponse(data)


class AnswerPaperDetail(DetailView):
    """ View to show answerpaper """
    model = AnswerPaper
    context_object_name = 'answerpaper'
    template_name = 'champsquarebackend/quiz/answerpaper.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    
    def get_participant(self):
        return self.object.participant
        
