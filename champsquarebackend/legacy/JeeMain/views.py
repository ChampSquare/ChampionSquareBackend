from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone


from .models import Result
from champsquarebackend.legacy.Uscholar.models import Question, AnswerPaper


@login_required
def show_exam_login_screen(request, question_paper_id=None):
    context = {"user": request.user,
               "question_paper_id": question_paper_id}
    return render(request, "login.html", context)


@login_required
def show_instruction(request, question_paper_id=None):
    context = {"question_paper_id": question_paper_id}
    return render(request, "instructions.html", context)


# @login_required
# def start_exam(request, question_paper_id=None):
#     """Check the user's credential and start the exam"""


def save_exam_result(request):
    user = request.user
    answer_paper_id = request.GET.get('paper_id', None)
    paper = AnswerPaper.objects.get(id=answer_paper_id)
    num_attempt = int(request.GET.get('num_attempt', None))
    num_correct = int(request.GET.get('num_correct', None))
    num_wrong = int(request.GET.get('num_wrong', None))
    marks_obtained = int(request.GET.get('marks_obtained', None))

    result = Result.objects.filter(user=user, answer_paper=paper).first()
    if result is None:
        result = Result(user=user, answer_paper=paper,
                        num_attempt=num_attempt, num_correct=num_correct,
                        num_wrong=num_wrong, marks_obtained=marks_obtained)
        result.save()
        complete_exam(request, paper)
    data = {
        'success': True
    }

    return JsonResponse(data)


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