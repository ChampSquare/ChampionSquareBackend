from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from champsquarebackend.core.loading import get_model, get_class

Question = get_model('question', 'question')
Quiz = get_model('quiz', 'quiz')
AnswerPaper = get_model('quiz', 'AnswerPaper')
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


# Legacy code
# todo: remove these and find better way to add answers
def complete_exam(request, answer_paper):
    answer_paper.update_marks()
    answer_paper.set_end_time(timezone.now())


def save_answer(request):
    answer_paper_id = request.GET.get('answer_paper_id', None)
    q_id = request.GET.get('question_id')
    answer_key = request.GET.get('answer_key')
    status = request.GET.get('status')
    time_spent = request.GET.get('time_spent')

    paper = AnswerPaper.objects.get(id=answer_paper_id)
    paper.add_answer_key(q_id, answer_key, status, time_spent)
    data = {
        'success': True
    }

    return JsonResponse(data)


def clear_answer(request):
    answer_paper_id = request.GET.get('answer_paper_id', None)
    q_id = request.GET.get('question_id')
    paper = AnswerPaper.objects.get(id=answer_paper_id)
    paper.clear_answer(q_id)
    data = {
        'success': True
    }

    return JsonResponse(data)


def save_unanswered(request):
    answer_paper_id = request.GET.get('answer_paper_id', None)
    q_id = request.GET.get('question_id')
    time_spent = request.GET.get('time_spent')
    paper = AnswerPaper.objects.get(id=answer_paper_id)
    paper.save_unanswered(q_id, time_spent)
    data = {
        'success': True
    }

    return JsonResponse(data)


def save_instruction_state(request):
    answer_paper_id = request.GET.get('answer_paper_id', None)
    paper = AnswerPaper.objects.get(id=answer_paper_id)
    paper.instruction_read = True
    paper.save()
    data = {
        'success': True
    }
    return JsonResponse(data)

