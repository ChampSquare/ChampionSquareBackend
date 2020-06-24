from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse

from .models import Question, Subject, Quiz
from .forms import QuestionForm, QuestionFilterForm, SubjectForm, QuizForm
from .shortcuts import get_objet_or_none

@staff_member_required
def add_or_edit_question(request, question_id=None):
    """
        view to create or update question
    """
    user = request.user
    question = get_objet_or_none(Question, pk=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = user
            question.save()
            # many-to-many field save function used to save the tags
            form.save_m2m()
            messages.success(request, 'Question saved successfully')
            return redirect(reverse('Uscholar:edit_question', kwargs={'question_id': question.id}))

    form = QuestionForm(instance=question)
    context = {'qform': form}
    return render(request, "quiz/add_question.html", context)

@staff_member_required
def show_questions(request):
    """
        display list of all questions in database
    """
    user = request.user
    context = {}

    if request.method == 'POST':
        # delete question/s if requestion is delete
        if request.POST.get('delete') == 'delete':
            data = request.POST.getlist('question')
            if data is not None:
                questions = Question.objects.filter(id__in=data, user_id=user.id)
                for question in questions:
                    # question.active = False
                    question.delete()

    context['questions'] = Question.objects.order_by('id')
    context['form'] = QuestionFilterForm(user=user)

    return render(request, 'quiz/showquestions.html', context)

@staff_member_required
def add_or_edit_subject(request, subject_id=None):
    """
        create or update subject
    """
    subject = get_objet_or_none(Subject, pk=subject_id)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.save()
            messages.success(request, 'Subject add successfully!')

    form = SubjectForm(instance=subject)
    context = {'form': form}
    return render(request, "quiz/add_subject.html", context)

@staff_member_required
def add_or_edit_quiz(request, quiz_id=None):
    """
        create or update quiz
    """
    user = request.user
    context = {}

    quiz = get_objet_or_none(Quiz, pk=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, 'Quiz successfully saved')
            return redirect(reverse('Uscholar:quiz_detail', kwargs={'quiz_id': quiz.id}))

        else:
            messages.error(request, 'Failed to add quiz')

    context['form'] = QuizForm(instance=quiz)
    return render(request, "quiz/add_quiz.html", context)


@staff_member_required
def show_quizzes(request):
    """
        show list of all quizzes stored in database
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)


    


