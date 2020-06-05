import csv
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Sum, Max, Q, F
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms.models import inlineformset_factory
from django.utils import timezone
from tablib import Dataset
from django.core.exceptions import ObjectDoesNotExist

# import cStringIO as StringIO
from io import StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

import json
import six
# Local imports.
from .models import get_model_class, Quiz, Question, QuestionPaper, QuestionSet, Course
from .models import Profile, Answer, AnswerPaper,  \
                         has_profile
from .forms import UserRegisterForm, UserLoginForm, QuizForm,\
                QuestionForm, QuestionFilterForm, CourseForm, ProfileForm, \
                get_object_form,  QuestionPaperForm, AddUserForm

from champsquarebackend.legacy.Unicorn.models import Student
from champsquarebackend.legacy.JeeMain.models import Result

URL_ROOT = ''
User = get_user_model()

def my_redirect(url):
    """An overridden redirect to deal with URL_ROOT-ing. See settings.py
    for details."""
    return redirect(URL_ROOT+url)


def my_render_to_response(request, template, context=None, **kwargs):
    """Overridden render_to_response.
    """
    if context is None:
        context = {'URL_ROOT': URL_ROOT}
    else:
        context['URL_ROOT'] = URL_ROOT
    return render(request, template, context)


def is_moderator(user):
    """Check if the user is having moderator rights"""
    if user.groups.filter(name='moderator').exists():
        return True


def add_to_group(users):
    """ add users to moderator group """
    group = Group.objects.get(name="moderator")
    for user in users:
        if not is_moderator(user):
            user.groups.add(group)


def index(request):
    """The start page.
    """
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='moderator').count() > 0:
            return my_redirect('/exam/manage/')
        return my_redirect("/exam/quizzes/")

    return my_redirect("/")

@login_required
def view_webcam_feed(request):
    user = request.user
    if user.groups.filter(name='moderator').count() > 0:
        return render(request, 'webcam.html', {})
    return my_redirect('/')

@login_required
def view_stored_video(request):
    user = request.user
    if user.groups.filter(name='moderator').count() > 0:
        return render(request, 'video_history.html', {})
    return my_redirect('/')

@login_required
def video_test(request):
    user = request.user
    if user.groups.filter(name='moderator').count() > 0:
        return render(request, 'videoroomtest.html', {})
    return my_redirect('/')




def instructions(request):
    return my_render_to_response(request, "iframesInstruction.html", {})



def homepage(request):
    """The homepage for unauthenticatd users """
    return render(request, "home/index.html", {})


def user_register(request):
    """ Register a new user.
    Create a user and corresponding profile and store roll_number also."""

    user = request.user
    ci = RequestContext(request)
    if user.is_authenticated:
        return my_redirect("/exam/quizzes/")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            u_name, pwd = form.save()
            new_user = authenticate(username=u_name, password=pwd)
            login(request, new_user)
            return my_redirect("/exam/quizzes/")
        else:
            return my_render_to_response(request, 'Uscholar/register.html', {'form': form},
                                         context_instance=ci)
    else:
        form = UserRegisterForm()
        return my_render_to_response(request, 'Uscholar/register.html', {'form': form},
                                      context_instance=ci)

@login_required
def add_user(request):
    """ Add a new user """
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()

    form = AddUserForm()
    return render(request, 'Uscholar/register.html', {'form': form})



def user_logout(request):
    """Show a page to inform user that the quiz has been compeleted."""
    logout(request)
    context = {'message': "You have been logged out successfully"}
    return my_render_to_response(request, 'Uscholar/complete.html', context)

@login_required
def show_students(request):
    students = Student.objects.all()
    for student in students:
        if not User.objects.filter(username=student.roll_number).exists():
            new_user = User.objects.create_user(student.roll_number, "ujjawal@example.com", student.roll_number)
            new_user.save()
            new_profile = Profile(user=new_user)
            new_profile.student = student
            new_profile.pwd = student.roll_number
            new_profile.save()

        else:
            user = User.objects.get(username=student.roll_number)
            try:
                new_profile = user.profile
            except ObjectDoesNotExist:
                new_profile = Profile(user=user)
                new_profile.student = student
                new_profile.pwd = student.roll_number
                new_profile.save()
                user.set_password(student.roll_number)
                user.save()

    users = User.objects.all()
    return render(request, 'Uscholar/show_students.html', {'users': users})


@login_required
def quizlist_user(request, enrolled=None):
    """Show All Quizzes that is available to logged-in user."""
    user = request.user
    if enrolled is not None:
        courses = user.students.all()
        title = 'Enrolled Courses'
    else:
        courses = Course.objects.filter(active=True, is_trial=False)
        title = 'All Courses'
    context = {'user': user, 'courses': courses, 'title': title}
    return redirect('/#mocktests')


@login_required
def results_user(request):
    """Show list of Results of Quizzes that is taken by logged-in user."""
    user = request.user
    papers = AnswerPaper.objects.get_user_answerpapers(user)
    context = {'papers': papers}
    return my_render_to_response(request, "Uscholar/results_user.html", context)


@login_required
def add_question(request, question_id=None):
    user = request.user
    ci = RequestContext(request)
    test_case_type = None

    if question_id is None:
        question = Question(user=user)
        question.save()
    else:
        question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        qform = QuestionForm(request.POST, request.FILES, instance=question)
        if qform.is_valid():
            question = qform.save(commit=False)
            question.user = user
            question.save()
            # many-to-many field save function used to save the tags
            qform.save_m2m()

        else:
            context = {'qform': qform, 'question': question}
            return my_render_to_response(request, "Uscholar/add_question.html", context,
                                         context_instance=ci)

    qform = QuestionForm(instance=question)
    context = {'qform': qform, 'question': question}
    return my_render_to_response(request, "Uscholar/add_question.html", context, context_instance=ci)


@login_required
def add_quiz(request, course_id, quiz_id=None):
    """To add a new quiz in the database.
    Create a new quiz and store it."""
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    ci = RequestContext(request)
    if not is_moderator(user) or (user != course.creator and user not in course.teachers.all()):
        raise Http404('You are not allowed to view this course !')
    context = {}
    if request.method == "POST":
        if quiz_id is None:
            form = QuizForm(request.POST, user=user, course=course_id)
            if form.is_valid():
                form.save()
                return my_redirect("/exam/manage/courses/")
            else:
                context["form"] = form
                return my_render_to_response(request, 'Uscholar/add_quiz.html',
                                             context,
                                             context_instance=ci)
        else:
            quiz = Quiz.objects.get(id=quiz_id)
            form = QuizForm(request.POST, user=user, course=course_id,
                            instance=quiz)
            if form.is_valid():
                form.save()
                context["quiz_id"] = quiz_id
                return my_redirect("/exam/manage/courses/")
    else:
        if quiz_id is None:
            form = QuizForm(course=course_id, user=user)
        else:
            quiz = Quiz.objects.get(id=quiz_id)
            form = QuizForm(user=user,course=course_id, instance=quiz)
            context["quiz_id"] = quiz_id
        context["form"] = form
        return my_render_to_response(request, 'Uscholar/add_quiz.html',
                                     context,
                                     context_instance=ci)


@login_required
def show_all_questionpapers(request, questionpaper_id=None):
    user = request.user
    ci = RequestContext(request)
    if not user.is_authenticated or not is_moderator(user):
        raise Http404('You are not allowed to view this page!')

    if questionpaper_id is None:
        qu_papers = QuestionPaper.objects.filter(is_trial=False)
        context = {'papers': qu_papers}
        return my_render_to_response(request, 'Uscholar/showquestionpapers.html', context,
                                     context_instance=ci)
    else:
        qu_papers = QuestionPaper.objects.get(id=questionpaper_id)
        quiz = qu_papers.quiz
        fixed_questions = qu_papers.get_ordered_questions()
        context = {'quiz': quiz, 'fixed_questions': fixed_questions}
        return my_render_to_response(request, 'Uscholar/editquestionpaper.html', context,
                                     context_instance=ci)


@login_required
def prof_manage(request, msg=None):
    """Take credentials of the user with professor/moderator
    rights/permissions and log in."""
    user = request.user
    ci = RequestContext(request)
    if user.is_authenticated and is_moderator(user):
        question_papers = QuestionPaper.objects.filter(quiz__course__creator=user,
                                                       quiz__is_trial=False
                                                       )
        trial_paper = AnswerPaper.objects.filter(user=user,
                                                 question_paper__quiz__is_trial=True
                                                 )
        if request.method == "POST":
            delete_paper = request.POST.getlist('delete_paper')
            for answerpaper_id in delete_paper:
                answerpaper = AnswerPaper.objects.get(id=answerpaper_id)
                qpaper = answerpaper.question_paper
                if qpaper.quiz.course.is_trial == True:
                    qpaper.quiz.course.delete()
                else:
                    if qpaper.answerpaper_set.count() == 1:
                        qpaper.quiz.delete()
                    else:
                        answerpaper.delete()
        users_per_paper = []
        for paper in question_papers:
            answer_papers = AnswerPaper.objects.filter(question_paper=paper)
            users_passed = AnswerPaper.objects.filter(question_paper=paper,
                    passed=True).count()
            users_failed = AnswerPaper.objects.filter(question_paper=paper,
                    passed=False).count()
            temp = paper, answer_papers, users_passed, users_failed
            users_per_paper.append(temp)
        context = {'user': user, 'users_per_paper': users_per_paper,
                   'trial_paper': trial_paper, 'msg': msg
                   }
        return my_render_to_response(request, 'Uscholar/moderator_dashboard.html', context, context_instance=ci)
    return my_redirect('/exam/login/')

@csrf_exempt
def user_login(request):
    """Take the credentials of the user and log the user in."""

    user = request.user
    ci = RequestContext(request)
    students = Student.objects.all()
    if user.is_authenticated:
        if user.groups.filter(name='moderator').count() > 0:
            return my_redirect('/exam/manage/')
        return my_redirect("/exam/start/1")  #hardcoded url

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            login(request, user)
            if user.groups.filter(name='moderator').count() > 0:
                return my_redirect('/exam/manage/')
            return my_redirect('/exam/start/1/')  #harcoded url 
        else:
            context = {"form": form}
            return my_render_to_response(request, 'login.html', context,
                                         context_instance=ci)
    else:
        form = UserLoginForm()
        context = {"form": form}
        return my_render_to_response(request, 'login.html', context,
                                     context_instance=ci)

@login_required
def enroll_student(request, course_id):
    user = request.user
    ci = RequestContext(request)
    course = get_object_or_404(Course, pk=course_id)
    if course.is_self_enroll():
        was_rejected = False
        course.enroll(was_rejected, user)

@login_required
def show_results(request, questionpaper_id=None):
    user = request.user
    ci = RequestContext(request)
    if not user.is_authenticated or not is_moderator(user):
        raise Http404('You are not allowed to view this page!')

    if questionpaper_id is None:
        q_paper = QuestionPaper.objects.filter(Q(quiz__course__creator=user) |
                                               Q(quiz__course__teachers=user),
                                               quiz__is_trial=False
                                               ).distinct()
        context = {'papers': [],
                   'quiz': None,
                   'quizzes': q_paper}
        return my_render_to_response(request, 'Uscholar/showresult.html', context,
                                     context_instance=ci)
    # quiz_id is not None.
    try:
        q_paper = QuestionPaper.objects.filter(Q(quiz__course__creator=user) |
                                               Q(quiz__course__teachers=user),
                                               quiz__is_trial=False,
                                               id=questionpaper_id).distinct()
    except QuestionPaper.DoesNotExist:
        papers = []
        q_paper = None
        latest_attempts = []
    else:
        result_objects = Result.objects.filter(answer_paper__question_paper=q_paper)\
            .order_by('-marks_obtained')
        results = []
        roll_numbers = []
        for result in result_objects:
            results.append(result)
        return render(request, 'Uscholar/showresult.html', {'results': results})


@login_required
def start(request, questionpaper_id=None, attempt_num=None):
    """Check the user cedentials and if any quiz is available,
        start the exam."""
    user = request.user
    ci = RequestContext(request)
    # check conditions
    try:
        quest_paper = QuestionPaper.objects.get(id=questionpaper_id)
    except QuestionPaper.DoesNotExist:
        msg = 'Quiz not found, please contact your ' \
              'instructor/administrator.'
        return redirect('/')
    if not quest_paper.get_ordered_questions():
        msg = 'Quiz does not have Questions, please contact your ' \
              'instructor/administrator.'
        return redirect('/')
    if not quest_paper.quiz.course.is_enrolled(user):
        enroll_student(request, quest_paper.quiz.course.id)
    # prerequisite check and passing criteria

    # if quest_paper.quiz.is_expired():
    #     if is_moderator(user):
    #         return redirect("/exam/manage")
    #     return redirect("/exam")
    
    
    # if any previous attempt
    last_attempt = AnswerPaper.objects.get_user_last_attempt(
        questionpaper=quest_paper, user=user)
    if last_attempt:
        if quest_paper.quiz.type == "iit":
            return show_question(request, last_attempt.current_question(), last_attempt)
        else:
            return show_jee_main_question(request, last_attempt)

    # elif last_attempt and not last_attempt.is_attempt_inprogress():
    #     msg = 'You have already submitted this exam.'
    #     return complete(request, msg, attempt_num, quest_paper.id)

    # allowed to start
    # if not quest_paper.can_attempt_now(user):
    #     if is_moderator(user):
    #         return redirect("/exam/manage")
    #     return redirect("/exam/quizzes")
    if attempt_num is None:
        attempt_number = 1 if not last_attempt else last_attempt.attempt_number + 1
        context = {'user': user, 'questionpaper': quest_paper,
                   'attempt_num': attempt_number}
        ip = request.META['REMOTE_ADDR']
        new_paper = quest_paper.make_answerpaper(user, ip, attempt_number)

        if quest_paper.quiz.type == "iit":
            return my_render_to_response(request, 'Uscholar/intro.html', context,
                                         context_instance=ci)
        else:
            return show_jee_main_question(request, new_paper)
    else:
        # if not hasattr(user, 'profile'):
        #     msg = 'You do not have a profile and cannot take the quiz!'
        #     raise Http404(msg)
        paper = AnswerPaper.objects.filter(user=request.user, attempt_number=attempt_num,
                                           question_paper=questionpaper_id).last()

        if quest_paper.quiz.type == "iit":
            return show_question(request, paper.current_question(), paper)
        else:
            return show_jee_main_question(request, paper)


@login_required
def show_question(request, question, paper, error_message=None, notification=None):
    """Show a question if possible."""
    user = request.user
    if not question:
        msg = 'Congratulations!  You have successfully completed the quiz.'
        return complete(request, msg, paper.attempt_number, paper.question_paper.id)

    if not paper.question_paper.quiz.active:
        reason = 'The quiz has been deactivated!'
        return complete(request, reason, paper.attempt_number, paper.question_paper.id)

    if paper.time_left() <= 0 and not is_moderator(user):
        reason = 'Your time is up!'
        return complete(request, reason, paper.attempt_number, paper.question_paper.id)

    test_cases = question.get_test_cases()
    questions = paper.questions.filter(question_section=question.question_section).filter(subject=question.subject)
    context = {'question': question, 'questions': questions, 'paper': paper, 'error_message': error_message,
                'test_cases': test_cases, 'notification': notification}
    count = 0
    for q in questions:
        if q.subject == question.subject:
            count += 1
    answers = paper.get_previous_answers(question)
    context['total_marks'] = int(count*question.points)
    context['startId'] = paper.next_section_id(question.question_section)
    context['count'] = count
    if answers:
        last_attempt = answers[0].answer
        context['last_attempt'] = last_attempt.encode('unicode-escape')

    ci = RequestContext(request)
    return my_render_to_response(request, 'Uscholar/question.html', context,
                                 context_instance=ci)


@login_required
def show_jee_main_question(request, paper, error_message=None, notification=None):

    if not paper.question_paper.quiz.active:
        reason = 'The quiz has been deactivated!'
        return complete(request, reason, paper.attempt_number, paper.question_paper.id)

    # if paper.time_left() <= 0 and not is_moderator(request.user):
    #     reason = 'Your time is up!'
    #     return complete(request, reason, paper.attempt_number, paper.question_paper.id)
    question_answers = zip(paper.question_paper.fixed_questions.all().order_by('id'),
                           paper.answers.all().order_by('question__id'))

    question_answers_2 = zip(paper.question_paper.fixed_questions.all().order_by('id'),
                           paper.answers.all().order_by('question__id'))

    context = {'paper': paper,
            'question_answers': question_answers, 'question_answers_2': question_answers_2}
    ci = RequestContext(request)

    return my_render_to_response(request, "jee_main_exam.html", context, context_instance=ci)


# @login_required
# def check(request, q_id, attempt_num=None, questionpaper_id=None, marked_for_review=False):
#     """Checks the answers of the user for particular question"""
#     user = request.user
#     paper = get_object_or_404(AnswerPaper, user=request.user, attempt_number=attempt_num,
#                               question_paper=questionpaper_id)
#     current_question = get_object_or_404(Question, pk=q_id)
#     next_question = paper.next_question(q_id)

#     if request.method == 'POST':
#         # Add the answer submitted, regardless of it being correct or not.

#         if not marked_for_review:
#             paper.remove_mark_for_review(current_question.id)

#         if current_question in paper.questions_answered.all():
#             clear_response(request, q_id, attempt_num, questionpaper_id)

#         if request.POST.get('answer') == None:
#             return show_question(request, next_question, paper)

#         if current_question.type == 'mcq':
#             user_answer = request.POST.get('answer')
#         elif current_question.type == 'integer':
#             try:
#                 user_answer = int(request.POST.get('answer'))
#             except ValueError:
#                 user_answer = 0

#         elif current_question.type == 'mcc':
#             user_answer = request.POST.getlist('answer')

#         elif current_question.type == 'paragraph':
#             user_answer = request.POST.get('answer')

#         elif current_question.type == 'match':
#             user_answer = request.POST.get('answer')

#         else:
#             user_answer = None
#         if not user_answer:
#             user_answer = 0

#         new_answer = Answer(question=current_question, answer=user_answer,
#                             correct=False, error=json.dumps([]))

#         result = paper.validate_answer(user_answer, current_question)
#         if result.get('success'):
#             marks = current_question.points
#             new_answer.set_marks(marks)
#             new_answer.correct = result.get('success')
#             error_message = None
#             new_answer.error = json.dumps(result.get('error'))
#             next_question = paper.add_completed_question(current_question.id)

#         else:
#             marks = result.get('negative')+result.get('partial')
#             new_answer.set_marks(marks)
#             error_message = result.get('error') if current_question.type == 'code' \
#                 or current_question.type == 'upload' else None
#             new_answer.error = json.dumps(result.get('error'))
#             next_question = current_question if current_question.type == 'code' \
#                 or current_question.type == 'upload' \
#                 else paper.add_completed_question(current_question.id)

#         new_answer.save()
#         paper.answers.add(new_answer)

#         paper.update_marks('inprogress')
#         paper.set_end_time(timezone.now())
#         return show_question(request, next_question, paper, error_message)
#     else:
#         return show_question(request, current_question, paper)


def quit(request, reason=None, attempt_num=None, questionpaper_id=None):
    """Show the quit page when the user logs out."""
    paper = AnswerPaper.objects.get(user=request.user,
                                    attempt_number=attempt_num,
                                    question_paper=questionpaper_id)

    context = {'paper': paper, 'message': reason}
    return my_render_to_response(request, 'Uscholar/quit.html', context,
                                 context_instance=RequestContext(request))


@login_required
def complete(request, reason=None, attempt_num=None, questionpaper_id=None):
    """Show a page to inform user that the quiz has been compeleted."""
    user = request.user
    if questionpaper_id is None:
        message = reason or "An Unexpected Error occurred. Please contact your '\
            'instructor/administrator.'"
        context = {'message': message}
        return my_render_to_response(request, 'Uscholar/complete.html', context)
    else:
        q_paper = QuestionPaper.objects.get(id=questionpaper_id)
        paper = AnswerPaper.objects.get(user=user, question_paper=q_paper,
                                        attempt_number=1)
        paper.update_marks()
        paper.set_end_time(timezone.now())
        message = reason or "Quiz has been submitted"
        context = {'message':  message, 'paper': paper}
        return my_render_to_response(request, 'Uscholar/complete.html', context)


@login_required
def add_course(request, course_id=None):
    user = request.user
    ci = RequestContext(request)
    if course_id:
        course = Course.objects.get(id=course_id)
    else:
        course = None

    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.creator = user
            new_course.save()
            return my_redirect('/exam/manage/')
        else:
            return my_render_to_response(request, 'Uscholar/add_course.html',
                                         {'form': form},
                                         context_instance=ci)
    else:
        form = CourseForm(instance=course)
        return my_render_to_response(request, 'Uscholar/add_course.html', {'form': form},
                                     context_instance=ci)


@login_required
def enroll_request(request, course_id):
    user = request.user
    ci = RequestContext(request)
    course = get_object_or_404(Course, pk=course_id)
    if not course.is_active_enrollment:
        msg = 'Enrollment for this course has been closed, please contact your '\
            'instructor/administrator.'
        return complete(request, msg, attempt_num=None, questionpaper_id=None)

    course.request(user)
    if is_moderator(user):
        return my_redirect('/exam/manage/courses')
    else:
        return my_redirect('/exam/quizzes/')


@login_required
def self_enroll(request, course_id):
    user = request.user
    ci = RequestContext(request)
    course = get_object_or_404(Course, pk=course_id)
    if course.is_self_enroll():
        was_rejected = False
        course.enroll(was_rejected, user)
    if is_moderator(user):
        return my_redirect('/exam/manage/')
    else:
        return my_redirect('/#mocktests')


@login_required
def courses(request):
    user = request.user
    ci = RequestContext(request)
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')
    courses = Course.objects.filter(creator=user)
    allotted_courses = Course.objects.filter(teachers=user)
    context = {'courses': courses, "allotted_courses": allotted_courses}
    return my_render_to_response(request, 'Uscholar/courses.html', context,
                                 context_instance=ci)


@login_required
def course_detail(request, course_id):
    user = request.user
    ci = RequestContext(request)

    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')

    course = get_object_or_404(Course, pk=course_id)
    if not course.is_creator(user) and not course.is_teacher(user):
        raise Http404('This course does not belong to you')

    return my_render_to_response(request, 'Uscholar/course_detail.html', {'course': course},
                                context_instance=ci)


@login_required
def enroll(request, course_id, user_id=None, was_rejected=False):
    user = request.user
    ci = RequestContext(request)
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')

    course = get_object_or_404(Course, pk=course_id)
    if not course.is_active_enrollment:
        msg = 'Enrollment for this course has been closed, please contact your '\
            'instructor/administrator.'
        return complete(request, msg, attempt_num=None, questionpaper_id=None)

    if not course.is_creator(user) and not course.is_teacher(user):
        raise Http404('This course does not belong to you')

    if request.method == 'POST':
        enroll_ids = request.POST.getlist('check')
    else:
        enroll_ids = [user_id]
    if not enroll_ids:
        return my_render_to_response(request, 'Uscholar/course_detail.html', {'course': course},
                                            context_instance=ci)
    users = User.objects.filter(id__in=enroll_ids)
    course.enroll(was_rejected, *users)
    return course_detail(request, course_id)


@login_required
def reject(request, course_id, user_id=None, was_enrolled=False):
    user = request.user
    ci = RequestContext(request)
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')

    course = get_object_or_404(Course, pk=course_id)
    if not course.is_creator(user) and not course.is_teacher(user):
        raise Http404('This course does not belong to you')

    if request.method == 'POST':
        reject_ids = request.POST.getlist('check')
    else:
        reject_ids = [user_id]
    if not reject_ids:
        return my_render_to_response(request, 'Uscholar/course_detail.html', {'course': course},
                                            context_instance=ci)
    users = User.objects.filter(id__in=reject_ids)
    course.reject(was_enrolled, *users)
    return course_detail(request, course_id)


@login_required
def toggle_course_status(request, course_id):
    user = request.user
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')

    course = get_object_or_404(Course, pk=course_id)
    if not course.is_creator(user) and not course.is_teacher(user):
        raise Http404('This course does not belong to you')

    if course.active:
        course.deactivate()
    else:
        course.activate()
    course.save()
    return course_detail(request, course_id)


@login_required
def show_statistics(request, questionpaper_id):
    user = request.user
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page')
    attempt_numbers = AnswerPaper.objects.get_attempt_numbers(questionpaper_id)
    quiz = get_object_or_404(QuestionPaper, pk=questionpaper_id).quiz
    
    question_stats = AnswerPaper.objects.get_question_statistics(
        questionpaper_id
    )
    context = {'question_stats': question_stats, 'quiz': quiz,
               'questionpaper_id': questionpaper_id}
    return my_render_to_response(request, 'Uscholar/statistics_question.html', context,
                                 context_instance=RequestContext(request))


@login_required
def monitor(request, questionpaper_id=None):
    """Monitor the progress of the papers taken so far."""

    user = request.user
    ci = RequestContext(request)
    if not user.is_authenticated or not is_moderator(user):
        raise Http404('You are not allowed to view this page!')


    if questionpaper_id is None:
        # q_paper = QuestionPaper.objects.filter(Q(quiz__course__creator=user) |
        #                                        Q(quiz__course__teachers=user)
        #                                        ).distinct()
        q_paper = QuestionPaper.objects.all()
        context = {'papers': [],
                   'quiz': None,
                   'quizzes': q_paper}
        return my_render_to_response(request, 'Uscholar/monitor.html', context,
                                     context_instance=ci)
    # quiz_id is not None.
    if request.method == 'POST':
        if request.POST.get('delete') == 'delete':
            data = request.POST.getlist('paper')
            if data is not None:
                papers_to_delete = AnswerPaper.objects.filter(id__in=data)
                for paper in papers_to_delete:
                    paper.delete() # remember to soft delete in production

    papers = AnswerPaper.objects.all().order_by(
        '-marks_obtained')
    try:
        # q_paper = QuestionPaper.objects.filter(Q(quiz__course__creator=user) |
        #                                        Q(quiz__course__teachers=user),
        #                                        id=questionpaper_id).distinct()
        q_paper = QuestionPaper.objects.all()
    except QuestionPaper.DoesNotExist:
        q_paper = None
        latest_attempts = []
    

    context = {'papers': papers, 'quiz': q_paper, 'quizzes': None }


    return my_render_to_response(request, 'Uscholar/monitor.html', context,
                                 context_instance=ci)


@csrf_exempt
def ajax_questions_filter(request):
    """Ajax call made when filtering displayed questions."""

    user = request.user
    filter_dict = {"user_id": user.id, "active": True}
    question_type = request.POST.get('question_type')
    marks = request.POST.get('marks')
    subject = request.POST.get('subject')

    if question_type != "select":
        filter_dict['type'] = str(question_type)

    if marks != "select":
        filter_dict['points'] = marks

    if subject != "select":
        filter_dict['subject'] = str(subject)

    questions = list(Question.objects.filter(**filter_dict))

    return my_render_to_response(request, 'Uscholar/ajax_question_filter.html',
                                  {'questions': questions})


def _get_questions(user, question_type, marks):
    if question_type is None and marks is None:
        return None
    if question_type:
        questions = Question.objects.filter(type=question_type,
             user=user,
             active=True
        )
        if marks:
            questions = questions.filter(points=marks)
    return questions


def _get_questions_subject(user, question_type, marks, subject):
    if question_type is None and marks is None and subject is None:
        return None
    if question_type:
        questions = Question.objects.filter(type=question_type,
             user=user,
             active=True
        )
        if marks:
            questions = questions.filter(points=marks)
        if subject:
            questions = questions.filter(subject=subject)
    return questions


def _remove_already_present(questionpaper_id, questions):
    if questionpaper_id is None:
        return questions
    questionpaper = QuestionPaper.objects.get(pk=questionpaper_id)
    questions = questions.exclude(
            id__in=questionpaper.fixed_questions.values_list('id', flat=True))
    return questions

@login_required
def design_paper(request, quiz_id, questionpaper_id=None):
    user = request.user

    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')
    quiz = Quiz.objects.get(id=quiz_id)
    if not quiz.course.is_creator(user) and not quiz.course.is_teacher(user):
        raise Http404('This course does not belong to you')
    filter_form = QuestionFilterForm(user=user)
    questions = None
    marks = None
    no_of_questions = None
    state = None
    if questionpaper_id is None:
        question_paper = QuestionPaper.objects.get_or_create(quiz_id=quiz_id)[0]
    else:
        question_paper = get_object_or_404(QuestionPaper, id=questionpaper_id)
    qpaper_form = QuestionPaperForm(instance=question_paper)

    if request.method == 'POST':

        filter_form = QuestionFilterForm(request.POST, user=user)
        qpaper_form = QuestionPaperForm(request.POST, instance=question_paper)
        question_type = request.POST.get('question_type', None)
        marks = request.POST.get('marks', None)
        subject = request.POST.get('subject', None)
        no_of_questions = request.POST.get('no_of_questions', None)
        state = request.POST.get('is_active', None)

        if 'add-fixed' in request.POST:
            question_ids = request.POST.get('checked_ques', None)

            questions_order = question_ids
            questions = Question.objects.filter(id__in=question_ids.split(','))
            question_paper.fixed_question_order = questions_order
            question_paper.save()
            question_paper.fixed_questions.add(*questions)

        if 'remove-fixed' in request.POST:
            question_ids = request.POST.getlist('added-questions', None)
            question_paper.save()
            question_paper.fixed_questions.remove(*question_ids)

        if 'save' in request.POST or 'back' in request.POST:
            qpaper_form.save()
            return my_redirect('/exam/manage/courses/')

        if marks:
            questions = _get_questions_subject(user, question_type, marks, subject)
            questions = _remove_already_present(questionpaper_id, questions)

        if subject:
            questions = _get_questions_subject(user, question_type, marks, subject)
            questions = _remove_already_present(questionpaper_id, questions)

        question_paper.update_total_marks()
        question_paper.update_total_questions()
        question_paper.save()
    fixed_questions = question_paper.get_ordered_questions()
    context = {'qpaper_form': qpaper_form, 'filter_form': filter_form, 'qpaper':
            question_paper, 'questions': questions, 'fixed_questions': fixed_questions,
            'state': state}
    return my_render_to_response(request, 'Uscholar/design_paper.html', context,
            context_instance=RequestContext(request))



@login_required
def design_questionpaper(request, quiz_id, questionpaper_id=None):
    user = request.user

    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')
    quiz = Quiz.objects.get(id=quiz_id)
    if not quiz.course.is_creator(user) and not quiz.course.is_teacher(user):
        raise Http404('This course does not belong to you')
    filter_form = QuestionFilterForm(user=user)
    questions = None
    marks = None
    no_of_questions = None
    state = None
    if questionpaper_id is None:
        question_paper = QuestionPaper.objects.get_or_create(quiz_id=quiz_id)[0]
    else:
        question_paper = get_object_or_404(QuestionPaper, id=questionpaper_id)
    qpaper_form = QuestionPaperForm(instance=question_paper)

    if request.method == 'POST':

        filter_form = QuestionFilterForm(request.POST, user=user)
        qpaper_form = QuestionPaperForm(request.POST, instance=question_paper)
        question_type = request.POST.get('question_type', None)
        marks = request.POST.get('marks', None)
        no_of_questions = request.POST.get('no_of_questions', None)
        state = request.POST.get('is_active', None)

        if 'add-fixed' in request.POST:
            question_ids = request.POST.get('checked_ques', None)

            questions_order = question_ids
            questions = Question.objects.filter(id__in=question_ids.split(','))
            question_paper.fixed_question_order = questions_order
            question_paper.save()
            question_paper.fixed_questions.add(*questions)

        if 'remove-fixed' in request.POST:
            question_ids = request.POST.getlist('added-questions', None)
            que_order = question_paper.fixed_question_order.split(",")
            for qid in question_ids:
                que_order.remove(qid)
            if que_order:
                question_paper.fixed_question_order = ",".join(que_order)
            else:
                question_paper.fixed_question_order = ""
            question_paper.save()
            question_paper.fixed_questions.remove(*question_ids)

        if 'save' in request.POST or 'back' in request.POST:
            qpaper_form.save()
            return my_redirect('/exam/manage/courses/')

        if marks:
            questions = _get_questions(user, question_type, marks)
            questions = _remove_already_present(questionpaper_id, questions)

        question_paper.update_total_marks()
        question_paper.update_total_questions()
        question_paper.save()
    fixed_questions = question_paper.get_ordered_questions()
    context = {'qpaper_form': qpaper_form, 'filter_form': filter_form, 'qpaper':
            question_paper, 'questions': questions, 'fixed_questions': fixed_questions,
            'state': state}
    return my_render_to_response(request, 'Uscholar/design_questionpaper.html', context,
            context_instance=RequestContext(request))


@login_required
def show_all_questions(request):
    """Show a list of all the questions currently in the database."""

    user = request.user
    ci = RequestContext(request)
    context = {}
    if not is_moderator(user):
        raise Http404("You are not allowed to view this page !")

    if request.method == 'POST':
        if request.POST.get('delete') == 'delete':
            data = request.POST.getlist('question')
            if data is not None:
                questions = Question.objects.filter(id__in=data, user_id=user.id)
                for question in questions:
                    # question.active = False
                    question.delete()

        if request.POST.get('test') == 'test':
            question_ids = request.POST.getlist("question")
            if question_ids:
                trial_paper = test_mode(user, False, question_ids, None)
                trial_paper.update_total_marks()
                trial_paper.update_total_questions()
                trial_paper.save()
                return my_redirect("/exam/start/1/{0}".format(trial_paper.id))
            else:
                context["msg"] = "Please select atleast one question to test"

    questions = Question.objects.order_by('id')
    form = QuestionFilterForm(user=user)
    context['papers'] = []
    context['question'] = None
    context['questions'] = questions
    context['form'] = form
    return my_render_to_response(request, 'Uscholar/showquestions.html', context,
                                 context_instance=ci)

def download_answer_paper(request, username):
    """Render user data."""
    
    ci = RequestContext(request)
    
    user = User.objects.get(username=username)
    paper = AnswerPaper.objects.filter(user=user, attempt_number=1).last()
    
    question_answers = zip(paper.question_paper.fixed_questions.all().order_by('id'),
                           paper.answers.all().order_by('question__id'))
    


    context = {'question_answers': question_answers, 'paper': paper}
    return my_render_to_response(request, 'Uscholar/user_data.html', context,
                                 context_instance=ci)


def user_data(request, user_id, questionpaper_id=None):
    """Render user data."""
    current_user = request.user
    ci = RequestContext(request)
    
    user = User.objects.get(id=user_id)
    paper = AnswerPaper.objects.filter(user=user, attempt_number=1,
                                           question_paper=questionpaper_id).last()
    
    question_answers = zip(paper.question_paper.fixed_questions.all().order_by('id'),
                           paper.answers.all().order_by('question__id'))
    


    context = {'question_answers': question_answers, 'paper': paper}
    return my_render_to_response(request, 'Uscholar/user_data.html', context,
                                 context_instance=ci)

def render_answer_paper_to_pdf(request):
    template = get_template('Uscholar/user_data.html')
    papers = AnswerPaper.objects.all().order_by(
        '-marks_obtained')
    for paper in papers:
        question_answers = zip(paper.question_paper.fixed_questions.all().order_by('id'),
                           paper.answers.all().order_by('question__id'))
        context = {'question_answers': question_answers, 'paper': paper}
    
        html  = template.render(context)
        result = StringIO()

        pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


@login_required
def download_csv(request, questionpaper_id=None):
    user = request.user
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')
    # quiz = Quiz.objects.get(questionpaper=questionpaper_id)

    papers = AnswerPaper.objects.all().order_by(
        '-marks_obtained')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'Result_roots_3rd.csv'
    writer = csv.writer(response)
    header = [
                'Roll Number',
                'name',
                'Total Attempt',
                'Correct',
                'Incorrect',
                'Marks in Physics',
                'Marks in Chemistry',
                'Marks in Maths',
                'Marks'
                # 'Phone Number',
                # 'Father Number'
    ]
    writer.writerow(header)
    count = 1
    for paper in papers:
        if hasattr(paper.user, 'profile'):
            row = [
                paper.user.username,
                paper.user.profile.student.name,
                paper.get_attempt_count(),
                paper.get_correct_answer_num(),
                paper.get_wrong_answer_num(),
                paper.get_marks_obtained_in_physics(),
                paper.get_marks_obtained_in_chemistry(),
                paper.get_marks_obtained_in_mathematics(),
                paper.marks_obtained
                # paper.user.profile.student.mobile_number,
                # paper.user.profile.student.father_number
                ]
            writer.writerow(row)
            count += 1
    return response


@login_required
def grade_user(request, quiz_id=None, user_id=None, attempt_number=None):
    """Present an interface with which we can easily grade a user's papers
    and update all their marks and also give comments for each paper.
    """
    current_user = request.user
    ci = RequestContext(request)
    if not current_user.is_authenticated or not is_moderator(current_user):
        raise Http404('You are not allowed to view this page!')
    course_details = Course.objects.filter(Q(creator=current_user) |
                                           Q(teachers=current_user),
                                           is_trial=False).distinct()
    context = {"course_details": course_details}
    if quiz_id is not None:
        questionpaper_id = QuestionPaper.objects.filter(quiz_id=quiz_id)\
                                                        .values("id")
        user_details = AnswerPaper.objects\
                                  .get_users_for_questionpaper(questionpaper_id)
        context = {"users": user_details, "quiz_id": quiz_id}
        if user_id is not None:

            attempts = AnswerPaper.objects.get_user_all_attempts\
                                            (questionpaper_id, user_id)
            try:
                if attempt_number is None:
                    attempt_number = attempts[0].attempt_number
            except IndexError:
                raise Http404('No attempts for paper')

            user = User.objects.get(id=user_id)
            data = AnswerPaper.objects.get_user_data(user, questionpaper_id,
                                                     attempt_number
                                                    )

            context = {'data': data, "quiz_id": quiz_id, "users": user_details,
                    "attempts": attempts, "user_id": user_id
                    }
    if request.method == "POST":
        papers = data['papers']
        for paper in papers:
            for question, answers, errors in six.iteritems(paper.get_question_answers()):
                marks = float(request.POST.get('q%d_marks' % question.id, 0))
                answers = answers[-1]
                answers.set_marks(marks)
                answers.save()

            paper.update_marks()
            paper.comments = request.POST.get(
                'comments_%d' % paper.question_paper.id, 'No comments')
            paper.save()

    return my_render_to_response(request, 'Uscholar/grade_user.html', context, context_instance=ci)


@login_required
def view_profile(request):
    """ view moderators and users profile """
    user = request.user
    ci = RequestContext(request)
    if is_moderator(user):
        template = 'manage.html'
    else:
        template = 'user.html'
    context = {'template': template}
    if has_profile(user):
        context['user'] = user
        return my_render_to_response(request, 'Uscholar/view_profile.html', context)
    else:
        form = ProfileForm(user=user)
        msg = True
        context['form'] = form
        context['msg'] = msg
        return my_render_to_response(request, 'Uscholar/editprofile.html', context,
                                    context_instance=ci)


@login_required
def edit_profile(request):
    """ edit profile details facility for moderator and students """

    user = request.user
    ci = RequestContext(request)
    if is_moderator(user):
        template = 'manage.html'
    else:
        template = 'user.html'
    context = {'template': template}
    if has_profile(user):
        profile = Profile.objects.get(user_id=user.id)
    else:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, user=user, instance=profile)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = user
            form_data.user.first_name = request.POST['first_name']
            form_data.user.last_name = request.POST['last_name']
            form_data.user.save()
            form_data.save()
            return my_render_to_response(request, 'Uscholar/profile_updated.html',
                                        context_instance=ci)
        else:
            context['form'] = form
            return my_render_to_response(request, 'Uscholar/editprofile.html', context,
                                        context_instance=ci)
    else:
        form = ProfileForm(user=user, instance=profile)
        context['form'] = form
        return my_render_to_response(request, 'Uscholar/editprofile.html', context,
                                    context_instance=ci)


@login_required
def search_teacher(request, course_id):
    """ search teachers for the course """
    user = request.user
    ci = RequestContext(request)

    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')

    context = {}
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course

    if user != course.creator and user not in course.teachers.all():
       raise Http404('You are not allowed to view this page!')

    if request.method == 'POST':
        u_name = request.POST.get('uname')
        if not len(u_name) == 0:
            teachers = User.objects.filter(Q(username__icontains=u_name)|
                Q(first_name__icontains=u_name)|Q(last_name__icontains=u_name)|
                Q(email__icontains=u_name)).exclude(Q(id=user.id)|Q(is_superuser=1)|
                                                    Q(id=course.creator.id))
            context['success'] = True
            context['teachers'] = teachers
    return my_render_to_response(request, 'Uscholar/addteacher.html', context,
                                 context_instance=ci)


@login_required
def add_teacher(request, course_id):
    """ add teachers to the course """

    user = request.user
    ci = RequestContext(request)

    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')

    context = {}
    course = get_object_or_404(Course, pk=course_id)
    if user == course.creator or user in course.teachers.all():
        context['course'] = course
    else:
        raise Http404('You are not allowed to view this page!')

    if request.method == 'POST':
        teacher_ids = request.POST.getlist('check')
        teachers = User.objects.filter(id__in=teacher_ids)
        add_to_group(teachers)
        course.add_teachers(*teachers)
        context['status'] = True
        context['teachers_added'] = teachers
    return my_render_to_response(request, 'Uscholar/addteacher.html', context,
                                    context_instance=ci)


@login_required
def remove_teachers(request, course_id):
    """  remove user from a course """

    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    if not is_moderator(user) and (user != course.creator and user not in course.teachers.all()):
        raise Http404('You are not allowed to view this page!')

    if request.method == "POST":
        teacher_ids = request.POST.getlist('remove')
        teachers = User.objects.filter(id__in=teacher_ids)
        course.remove_teachers(*teachers)
    return my_redirect('/exam/manage/courses')


def test_mode(user, godmode=False, questions_list=None, quiz_id=None):
    """creates a trial question paper for the moderators"""

    if questions_list is not None:
        trial_course = Course.objects.create_trial_course(user)
        trial_quiz = Quiz.objects.create_trial_quiz(trial_course, user)
        trial_questionpaper = QuestionPaper.objects\
                                           .create_trial_paper_to_test_questions\
                                            (trial_quiz, questions_list)
    else:
        trial_quiz = Quiz.objects.create_trial_from_quiz(quiz_id, user, godmode)
        trial_questionpaper = QuestionPaper.objects\
                                           .create_trial_paper_to_test_quiz\
                                            (trial_quiz, quiz_id)
    return trial_questionpaper

    


@login_required
def test_quiz(request, mode, quiz_id):
    """creates a trial quiz for the moderators"""
    godmode = True if mode == "godmode" else False
    current_user = request.user
    print("mode : " +mode)
    quiz = Quiz.objects.get(id=quiz_id)
    if (quiz.is_expired() or not quiz.active) and not godmode:
        return my_redirect('/exam/manage')

    trial_questionpaper = test_mode(current_user, godmode, None, quiz_id)
    print(trial_questionpaper)
    return my_redirect("/exam/start/{0}".format(trial_questionpaper.id))


@login_required
def view_answerpaper(request, questionpaper_id):
    user = request.user
    quiz = get_object_or_404(QuestionPaper, pk=questionpaper_id).quiz
    if quiz.view_answerpaper and user in quiz.course.students.all():
        data = AnswerPaper.objects.get_user_data(user, questionpaper_id)
        context = {'data': data, 'quiz': quiz}
        return my_render_to_response(request, 'Uscholar/view_answerpaper.html', context)
    else:
        return my_redirect('/exam/quizzes/')


@login_required
def create_demo_course(request):
    """ creates a demo course for user """
    user = request.user
    ci = RequestContext(request)
    if not is_moderator(user):
        raise("You are not allowed to view this page")
    demo_course = Course()
    success = demo_course.create_demo(user)
    if success:
        msg = "Created Demo course successfully"
    else:
        msg = "Demo course already created"
    return prof_manage(request, msg)


@login_required
def grader(request, extra_context=None):
    user = request.user
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')
    courses = Course.objects.filter(is_trial=False)
    user_courses = list(courses.filter(creator=user)) + list(courses.filter(teachers=user))
    context = {'courses': user_courses}
    if extra_context:
        context.update(extra_context)
    return my_render_to_response(request, 'Uscholar/regrade.html', context)


@login_required
def regrade(request, course_id, question_id=None, answerpaper_id=None, questionpaper_id=None):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    if not is_moderator(user) or (user != course.creator and user not in course.teachers.all()):
        raise Http404('You are not allowed to view this page!')
    details = []
    if answerpaper_id is not None and question_id is None:
        answerpaper = get_object_or_404(AnswerPaper, pk=answerpaper_id)
        for question in answerpaper.questions.all():
            details.append(answerpaper.regrade(question.id))
    if questionpaper_id is not None and question_id is not None:
        answerpapers = AnswerPaper.objects.filter(questions=question_id,
                question_paper_id=questionpaper_id)
        for answerpaper in answerpapers:
            details.append(answerpaper.regrade(question_id))
    if answerpaper_id is not None and question_id is not None:
        answerpaper = get_object_or_404(AnswerPaper, pk=answerpaper_id)
        details.append(answerpaper.regrade(question_id))
    return grader(request, extra_context={'details': details})

@login_required
def download_course_csv(request, course_id):
    user = request.user
    if not is_moderator(user):
        raise Http404('You are not allowed to view this page!')
    course = get_object_or_404(Course,pk=course_id)
    if not course.is_creator(user) and not course.is_teacher(user):
        raise Http404('The question paper does not belong to your course')
    students = course.get_only_students().annotate(roll_number=F('profile__roll_number'),
                                                   institute=F('profile__institute')
                                                    )\
                                         .values("id", "first_name", "last_name",
                                                 "email","institute",
                                                 "roll_number"
                                                 )
    quizzes = Quiz.objects.filter(course=course, is_trial=False)

    for student in students:
        total_course_marks = 0.0
        user_course_marks = 0.0
        for quiz in quizzes:
            quiz_best_marks = AnswerPaper.objects.get_user_best_of_attempts_marks\
                               (quiz, student["id"])
            user_course_marks += quiz_best_marks
            total_course_marks += quiz.questionpaper_set.values_list\
                                    ("total_marks", flat=True)[0]
            student["{}".format(quiz.description)] = quiz_best_marks
        student["total_scored"] = user_course_marks
        student["out_of"] = total_course_marks


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(
                                      (course.name).lower().replace('.', ''))
    header = ['first_name', 'last_name', "roll_number","email", "institute"]\
            +[quiz.description for quiz in quizzes] + ['total_scored', 'out_of']
    writer = csv.DictWriter(response,fieldnames=header, extrasaction='ignore')
    writer.writeheader()
    for student in students:
        writer.writerow(student)
    return response
