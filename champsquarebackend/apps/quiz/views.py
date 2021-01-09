from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from champsquarebackend.core.loading import get_model, get_class

Question = get_model('question', 'question')
Quiz = get_model('quiz', 'quiz')
AnswerPaper = get_model('quiz', 'AnswerPaper')
Participant = get_model('participate', 'participant')
QuizConditionsMixin = get_class('quiz.mixins', 'QuizConditionsMixin')

class QuizView(QuizConditionsMixin, ListView):
    """
        view to take quiz
    """
    model = Question
    context_object_name = "answers"
    template_name = 'champsquarebackend/quiz/quiz.html'
    # pre_conditions = ['is_participant', 'can_take_new', 'check_ip_restriction', 'can_resume']
    pre_conditions = ['is_participant', 'check_ip_restriction', 'can_resume']

    skip_conditions = []

    def get_queryset(self):
        return self.get_answerpaper().answers.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['quiz'] = self.get_quiz()
        ctx['participant'] = self.get_participant()
        ctx['answerpaper'] = self.get_answerpaper()
        ctx['video_monitoring'] = self.get_participant().video_monitoring_enabled
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

class SaveAnswerPaperStatusView(View):
    """
     save instruction read status
    """
    
    def get(self, request, *args, **kwargs):
        answer_paper_id = int(request.GET.get('answer_paper_id', None))
        status = request.GET.get('status', None)
        paper = AnswerPaper.objects.get(id=answer_paper_id)
        paper.set_status(status)
        data = {
            'success': True
        }
        return JsonResponse(data)
        
