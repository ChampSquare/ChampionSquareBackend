from __future__ import unicode_literals
from datetime import datetime, timedelta
import stat
from os.path import join, exists
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum

import json
from random import sample
from collections import Counter
from django.db import models
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from django.utils import timezone

from django.core.files import File
try:
    from StringIO import StringIO as string_io
except ImportError:
    from io import BytesIO as string_io
import pytz
import os
import sys
import six
import math

from champsquarebackend.legacy.Unicorn.models import Student

import traceback

User = get_user_model()


subjects = (
       ("physics", "Physics"),
       ("chemistry", "Chemistry"),
       ("mathematics", "Mathematics"),
       ("biology", "Biology"),
   )

question_types = (
        ("mcq", "Single Correct Choice"),
        ("mcc", "Multiple Correct Choices"),
        ("integer", "Answer in Integer"),
        ("paragraph", "Paragraph Type"),
        ("match", "Matching Type")
    )

answer_status = (
    ("0", "Not Visited"),
    ("1", "Not Answered"),
    ("2", "Answered"),
    ("3", "Marked For Review"),
    ("4", "Answered And Marked For Review")
)

quiz_type = (
    ("jee_main", "Jee Main"),
    ("iit", "IIT"),
    ("neet", "NEET")
)

enrollment_methods = (
    ("default", "Enroll Request"),
    ("open", "Open Course"),
    )

test_case_types = (
        ("mcqtestcase", "MCQ Testcase"),
        ("integertestcase", "Integer Testcase")
    )

question_section = (
    ("sec1", "Section One"),
    ("sec2", "Section Two"),
    ("sec3", "Section Three"),
    ("sec4", "Section Four")
)


attempts = [(i, i) for i in range(1, 6)]
attempts.append((-1, 'Infinite'))
days_between_attempts = [(j, j) for j in range(401)]

test_status = (
                ('inprogress', 'Inprogress'),
                ('completed', 'Completed'),
              )




def get_model_class(model):
    ctype = ContentType.objects.get(app_label="Uscholar", model=model)
    model_class = ctype.model_class()

    return model_class


def has_profile(user):
    """ check if user has profile """
    return True if hasattr(user, 'profile') else False



###############################################################################
class CourseManager(models.Manager):

    def create_trial_course(self, user):
        """Creates a trial course for testing questions"""
        trial_course = self.create(name="trial_course", enrollment="open",
                                   creator=user, is_trial=True)
        trial_course.enroll(False, user)
        return trial_course


###############################################################################
class Course(models.Model):
    """ Course for students"""
    name = models.CharField(max_length=128)
    enrollment = models.CharField(max_length=32, choices=enrollment_methods)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='students')
    requests = models.ManyToManyField(User, related_name='requests')
    rejected = models.ManyToManyField(User, related_name='rejected')
    created_on = models.DateTimeField(auto_now_add=True)
    teachers = models.ManyToManyField(User, related_name='teachers')
    is_trial = models.BooleanField(default=False)
    description = models.TextField(default=None, null=True, blank=True)
    instructions = models.TextField(default=None, null=True, blank=True)
    picture = models.ImageField('TestSeries picture',
                                upload_to='testseries_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)


    # The start date of the course enrollment.
    start_enroll_time = models.DateTimeField(
        "Start Date and Time for enrollment of course",
        default=timezone.now,
        null=True
    )

    # The end date and time of the course enrollment
    end_enroll_time = models.DateTimeField(
        "End Date and Time for enrollment of course",
        default=datetime(
            2199, 1, 1,
            tzinfo=pytz.timezone(timezone.get_current_timezone_name())
        ),
        null=True
    )

    objects = CourseManager()

    def request(self, *users):
        self.requests.add(*users)

    def get_requests(self):
        return self.requests.all()

    def is_active_enrollment(self):
        return self.start_enroll_time <= timezone.now() < self.end_enroll_time

    def enroll(self, was_rejected, *users):
        self.students.add(*users)
        if not was_rejected:
            self.requests.remove(*users)
        else:
            self.rejected.remove(*users)

    def get_enrolled(self):
        return self.students.all()

    def reject(self, was_enrolled, *users):
        self.rejected.add(*users)
        if not was_enrolled:
            self.requests.remove(*users)
        else:
            self.students.remove(*users)

    def get_rejected(self):
        return self.rejected.all()

    def is_enrolled(self, user):
        return user in self.students.all()

    def is_creator(self, user):
        return self.creator == user

    def is_teacher(self, user):
        return True if user in self.teachers.all() else False

    def is_self_enroll(self):
        return True if self.enrollment == enrollment_methods[1][0] else False

    def get_quizzes(self):
        return self.quiz_set.filter(is_trial=False).order_by('-id')

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_teachers(self, *teachers):
        self.teachers.add(*teachers)

    def get_teachers(self):
        return self.teachers.all()

    def remove_teachers(self, *teachers):
        self.teachers.remove(*teachers)

    def create_demo(self, user):
        course = Course.objects.filter(creator=user, name="Yaksh Demo course")
        if not course:
            course = Course.objects.create(name="Yaksh Demo course",
                                           enrollment="open",
                                           creator=user)
            quiz = Quiz()
            demo_quiz = quiz.create_demo_quiz(course)
            demo_ques = Question()
            # demo_ques.create_demo_questions(user)
            demo_que_ppr = QuestionPaper()
            # demo_que_ppr.create_demo_quiz_ppr(demo_quiz, user)
            success = True
        else:
            success = False
        return success

    def get_only_students(self):
        teachers = list(self.teachers.all().values_list("id", flat=True))
        teachers.append(self.creator.id)
        students = self.students.exclude(id__in=teachers)
        return students

    def __str__(self):
        return self.name


##############################################################################
class SubjectManager(models.Manager):

    def new_subject(self, subject="Physics"):
        """Creates a new subject for testing questions"""
        new_subject = self.create(subject)
        return new_subject

###############################################################################
class Subject(models.Model):
    subject = models.CharField(max_length=20, choices=subjects)

    objects = SubjectManager()

    def __str__(self):
        return self.subject

###############################################################################


class Profile(models.Model):
    """Profile for a user to store roll number and other details."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    pwd = models.CharField(max_length=25, blank=False, null=False)

    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)

    def get_user_dir(self):
        """Return the output directory for the user."""

        user_dir = join(settings.OUTPUT_DIR, str(self.user.username))
        if not exists(user_dir):
            os.makedirs(user_dir)
            os.chmod(user_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        return user_dir


def get_default_question_summary():
    if Question.objects.all():
        return Question.objects.all().latest('id').summary
    return "Roots Online Test - 2 Physics Sec - 1"


def get_default_question_subject():
    if Question.objects.all():
        return Question.objects.all().latest('id').subject
    return "physics"


def get_default_question_sec():
    if Question.objects.all():
        return Question.objects.all().latest('id').question_section
    return "sec1"


def get_default_question_type():
    if Question.objects.all():
        return Question.objects.all().latest('id').type
    return "mcq"


def get_default_negative_point():
    if Question.objects.all():
        if Question.objects.all().latest('id').type == "integer":
            return 0
    return -1



###############################################################################
class Question(models.Model):
    """Question for a quiz."""

    # A one-line summary of the question.
    summary = models.CharField(max_length=256, default=get_default_question_summary)

    # The question text, should be valid HTML.
    description = models.TextField(blank=True)

    picture = models.ImageField('Question Picture',
                                upload_to='question_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    type = models.CharField(max_length=24, choices=question_types, default=get_default_question_type)

    question_section = models.CharField(max_length=20, choices=question_section, default=get_default_question_sec, null=True, blank=True)

    # Number of points for the question.
    points = models.FloatField(default=4.0)
    negative_point = models.FloatField(default=get_default_negative_point)
    right_answer = models.CharField(max_length=10, null=True, blank=True)

    # The language for question.
    subject = models.CharField(max_length=24, default=get_default_question_subject, choices=subjects)

    # Is this question active or not. If it is inactive it will not be used
    # when creating a QuestionPaper.
    active = models.BooleanField(default=True)

    # Tags for the Question.
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    # user for particular question
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)

    def get_test_cases(self, **kwargs):
        tc_list = []
        for tc in self.testcase_set.values_list("type", flat=True).distinct():
            test_case_ctype = ContentType.objects.get(app_label="Uscholar",
                                                      model=tc)
            test_case = test_case_ctype.get_all_objects_for_this_type(
                question=self,
                **kwargs
            )
            tc_list.extend(test_case)
        return tc_list

    def get_right_answer(self):
        return self.right_answer

    def get_test_case(self, **kwargs):
        for tc in self.testcase_set.all():
            test_case_type = tc.type
            test_case_ctype = ContentType.objects.get(
                app_label="Uscholar",
                model=test_case_type
            )
            test_case = test_case_ctype.get_object_for_this_type(
                question=self,
                **kwargs
            )

        return test_case

    def __str__(self):
        return self.summary


###############################################################################
class Answer(models.Model):
    """Answers submitted by the users."""

    # The question for which user answers.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # The answer submitted by the user.
    answer = models.CharField(max_length=10, null=True, blank=True)

    # Error message when auto-checking the answer.
    error = models.TextField()

    # Marks obtained for the answer. This can be changed by the teacher if the
    # grading is manual.
    marks = models.FloatField(default=0.0)

    # Is the answer correct.
    correct = models.BooleanField(default=False)

    # Whether skipped or not.
    skipped = models.BooleanField(default=False)

    status = models.CharField(max_length=2, choices=answer_status, default="0")

    time_spent = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def set_marks(self, marks):
        self.marks = marks

    def set_answer(self, answer_key):
        self.answer = answer_key

    def set_time_spent(self, time_spent):
        self.time_spent = time_spent

    def mark_answer(self, is_correct):
        self.correct = is_correct

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return self.answer


###############################################################################
class QuizManager(models.Manager):
    def get_active_quizzes(self):
        return self.filter(active=True, is_trial=False)

    def create_trial_quiz(self, trial_course, user):
        """Creates a trial quiz for testing questions"""
        trial_quiz = self.create(course=trial_course,
                                 duration=1000,
                                 description="trial_questions",
                                 is_trial=True,
                                 time_between_attempts=0
                                 )
        return trial_quiz

    def create_trial_from_quiz(self, original_quiz_id, user, godmode):
        """Creates a trial quiz from existing quiz"""
        trial_quiz_name = "Trial_orig_id_{0}_{1}".format(
            original_quiz_id,
            "godmode" if godmode else "usermode"
        )

        if self.filter(description=trial_quiz_name).exists():
            trial_quiz = self.get(description=trial_quiz_name)

        else:
            trial_quiz = self.get(id=original_quiz_id)
            trial_quiz.course.enroll(False, user)
            trial_quiz.pk = None
            trial_quiz.description = trial_quiz_name
            trial_quiz.is_trial = True
            trial_quiz.prerequisite = None
            if godmode:
                trial_quiz.time_between_attempts = 0
                trial_quiz.duration = 1000
                trial_quiz.attempts_allowed = -1
                trial_quiz.active = True
                trial_quiz.start_date_time = timezone.now()
                trial_quiz.end_date_time = datetime(
                    2199, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc
                )
            trial_quiz.save()
        return trial_quiz


###############################################################################
class Quiz(models.Model):
    """A quiz that students will participate in. One can think of this
    as the "examination" event.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # The start date of the quiz.
    start_date_time = models.DateTimeField(
        "Start Date and Time of the quiz",
        default=timezone.now,
        null=True
    )

    # The end date and time of the quiz
    end_date_time = models.DateTimeField(
        "End Date and Time of the quiz",
        default=datetime(
            2199, 1, 1,
            tzinfo=pytz.timezone(timezone.get_current_timezone_name())
        ),
        null=True
    )

    type = models.CharField("Type of quiz", max_length=20, choices=quiz_type, default="iit")

    # This is always in minutes.
    duration = models.IntegerField("Duration of quiz in minutes", default=180)

    # Is the quiz active. The admin should deactivate the quiz once it is
    # complete.
    active = models.BooleanField(default=False)

    # Description of quiz.
    description = models.CharField(max_length=256)

    # Minimum passing percentage condition.
    pass_criteria = models.FloatField("Passing percentage", default=30)

    # List of prerequisite quizzes to be passed to take this quiz
    prerequisite = models.ForeignKey("Quiz", null=True, blank=True, on_delete=models.CASCADE)

    # Number of attempts for the quiz
    attempts_allowed = models.IntegerField(default=1, choices=attempts)

    time_between_attempts = models.IntegerField(
        "Number of Days", choices=days_between_attempts
    )

    is_trial = models.BooleanField(default=False)

    view_answerpaper = models.BooleanField('Allow student to view their answer\
                                            paper', default=False)

    allow_skip = models.BooleanField("Allow students to skip questions",
                                     default=True)

    objects = QuizManager()

    class Meta:
        verbose_name_plural = "Quizzes"

    def is_expired(self):
        return not self.start_date_time <= timezone.now() < self.end_date_time

    def is_started(self):
        return self.get_time_to_start() <= 0

    def get_time_to_start(self):
        """Return the time remaining for the user in seconds."""
        dt = self.start_date_time - timezone.now()
        try:
           mins = dt.total_seconds() / 60.0
        except AttributeError:
            # total_seconds is new in Python 2.7. :(
            mins = (dt.seconds + dt.days * 24 * 3600) / 60.0
        return mins


    def has_prerequisite(self):
        return True if self.prerequisite else False

    def create_demo_quiz(self, course):
        demo_quiz = Quiz.objects.create(
            start_date_time=timezone.now(),
            end_date_time=timezone.now() + timedelta(176590),
            duration=30, active=True,
            attempts_allowed=-1,
            time_between_attempts=0,
            description='Yaksh Demo quiz', pass_criteria=0,
            #language='Python', prerequisite=None,
            course=course
        )
        return demo_quiz

    def __str__(self):
        desc = self.description or 'Quiz'
        return '%s: on %s for %d minutes' % (desc, self.start_date_time,
                                             self.duration)


###############################################################################
class QuestionPaperManager(models.Manager):

    def _create_trial_from_questionpaper(self, original_quiz_id):
        """Creates a copy of the original questionpaper"""
        trial_questionpaper = self.get(quiz_id=original_quiz_id)
        fixed_ques = trial_questionpaper.get_ordered_questions()
        trial_questions = {"fixed_questions": fixed_ques}
        trial_questionpaper.pk = None
        trial_questionpaper.save()
        return trial_questionpaper, trial_questions

    def create_trial_paper_to_test_questions(self, trial_quiz,
                                             questions_list):
        """Creates a trial question paper to test selected questions"""
        if questions_list is not None:
            trial_questionpaper = self.create(quiz=trial_quiz,
                                              total_marks=10,
                                              )
            trial_questionpaper.fixed_question_order = ",".join(questions_list)
            trial_questionpaper.fixed_questions.add(*questions_list)
            return trial_questionpaper

    def create_trial_paper_to_test_quiz(self, trial_quiz, original_quiz_id):
        """Creates a trial question paper to test quiz."""
        if self.filter(quiz=trial_quiz).exists():
            trial_questionpaper = self.get(quiz=trial_quiz)
        else:
            trial_questionpaper, trial_questions = \
                self._create_trial_from_questionpaper(original_quiz_id)
            trial_questionpaper.quiz = trial_quiz
            trial_questionpaper.fixed_questions\
                .add(*trial_questions["fixed_questions"])
            trial_questionpaper.save()
        return trial_questionpaper


###############################################################################
class QuestionPaper(models.Model):
    """Question paper stores the detail of the questions."""

    # Question paper belongs to a particular quiz.
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # Questions that will be mandatory in the quiz.
    fixed_questions = models.ManyToManyField(Question)
    shuffle_questions = models.BooleanField(default=False, blank=False)
    question_section = models.ManyToManyField("QuestionSection")

    # Total marks for the question paper.
    total_marks = models.FloatField(default=0.0, blank=True)

    # Negative marking is enabled or not
    negative_marking = models.BooleanField(default=True)

    # total number of questions
    total_questions = models.IntegerField(default=0, blank=True)

    objects = QuestionPaperManager()

    def update_total_marks(self):
        """ Updates the total marks for the Question Paper"""
        marks = 0.0
        questions = self.fixed_questions.all()
        for question in questions:
            marks += question.points
        self.total_marks = marks

    def update_total_questions(self):
        """ Updates the total marks for the Question Paper"""
        self.total_questions = self.fixed_questions.count()

    def _get_questions_for_answerpaper(self):
        """ Returns fixed and random questions for the answer paper"""
        questions = self.get_ordered_questions()
        return questions

    def make_answerpaper(self, user, ip, attempt_num):
        """Creates an  answer paper for the user to attempt the quiz"""
        ans_paper = AnswerPaper(
            user=user,
            user_ip=ip,
            attempt_number=attempt_num
        )
        ans_paper.start_time = timezone.now()
        ans_paper.end_time = ans_paper.start_time + \
            timedelta(minutes=self.quiz.duration)
        ans_paper.question_paper = self
        ans_paper.save()
        questions = self._get_questions_for_answerpaper()
        for question in questions:
            ans_paper.questions.add(question)
            ans_paper.add_answer_key(question.id, "NA")
        return ans_paper

    def _is_questionpaper_passed(self, user):
        return AnswerPaper.objects.filter(question_paper=self, user=user,
                                          passed=True).exists()

    def _is_attempt_allowed(self, user):
        attempts = AnswerPaper.objects.get_total_attempt(questionpaper=self,
                                                         user=user)
        return attempts != self.quiz.attempts_allowed

    def can_attempt_now(self, user):
        if self._is_attempt_allowed(user):
            last_attempt = AnswerPaper.objects.get_user_last_attempt(
                user=user, questionpaper=self
            )
            if last_attempt:
                time_lag = (timezone.now() - last_attempt.start_time).days
                return time_lag >= self.quiz.time_between_attempts
            else:
                return True
        else:
            return False

    def _get_prequisite_paper(self):
        return self.quiz.prerequisite.questionpaper_set.get()

    def is_prerequisite_passed(self, user):
        if self.quiz.has_prerequisite():
            prerequisite = self._get_prequisite_paper()
            return prerequisite._is_questionpaper_passed(user)

    def get_ordered_questions(self):
        return self.fixed_questions.all().order_by('question_section')

    def __str__(self):
        return "Question Paper for " + self.quiz.description


###############################################################################
class QuestionSet(models.Model):
    """Question set contains a set of questions from which random questions
       will be selected for the quiz.
    """

    # Marks of each question of a particular Question Set
    marks = models.FloatField()

    # Set of questions for sampling randomly.
    questions = models.ManyToManyField(Question)

    def get_random_questions(self):
        """ Returns random questions from set of questions"""
        return sample(list(self.questions.all()), self.num_questions)


###############################################################################
class QuestionSection(models.Model):
    name = models.CharField(max_length=24)
    # Marks of each question of a particular Question Set
    marks = models.FloatField()
    # type of section
    type = models.CharField(max_length=24, choices=question_types)
    # total marks of section
    maximum_marks = models.IntegerField(null=True, blank=True)

    # Number of questions to be fetched for the quiz.
    num_questions = models.IntegerField(null=True, blank=True)

    # first question id
    first_question_id = models.IntegerField(null=True, blank=True)


class AnswerPaperManager(models.Manager):
    def get_all_questions(self, questionpaper_id):
        ''' Return a dict of question id as key and count as value'''
        papers = self.filter(question_paper_id=questionpaper_id)
        all_questions = list()
        questions = list()
        for paper in papers:
            all_questions += paper.get_questions()
        for question in all_questions:
            questions.append(question.id)
        return Counter(questions)

    def get_all_questions_answered(self, questionpaper_id):
        ''' Return a dict of answered question id as key and count as value'''
        papers = self.filter(question_paper_id=questionpaper_id)
        questions_answered = list()
        for paper in papers:
            for answer in paper.answers.filter(Q(status="2") | Q(status="4")):
                if answer.correct:
                    questions_answered.append(answer.question.id)
        return Counter(questions_answered)

    def get_all_questions_wrong_answered(self, questionpaper_id):
        ''' Return a dict of answered question id as key and count as value'''
        papers = self.filter(question_paper_id=questionpaper_id)
        questions_wrong_answered = list()
        for paper in papers:
            for answer in paper.answers.filter(Q(status="2") | Q(status="4")):
                if not answer.correct:
                    questions_wrong_answered.append(answer.question.id)
        return Counter(questions_wrong_answered)

    def get_all_questions_unanswered(self, questionpaper_id):
        ''' Return a dict of answered question id as key and count as value'''
        papers = self.filter(question_paper_id=questionpaper_id)
        questions_unanswered = list()
        for paper in papers:
            for answer in paper.answers.filter(Q(status="0") | Q(status="1") | Q(status="3")):
                questions_unanswered.append(answer.question.id)
        return Counter(questions_unanswered)

    def get_attempt_numbers(self, questionpaper_id, status='completed'):
        ''' Return list of attempt numbers'''
        attempt_numbers = self.filter(
            question_paper_id=questionpaper_id, status=status
        ).values_list('attempt_number', flat=True).distinct()
        return attempt_numbers

    def has_attempt(self, questionpaper_id, attempt_number,
                    status='completed'):
        ''' Whether question paper is attempted'''
        return self.filter(
            question_paper_id=questionpaper_id,
            attempt_number=attempt_number, status=status
        ).exists()

    def get_count(self, questionpaper_id, attempt_number, status='completed'):
        ''' Return count of answerpapers for a specfic question paper
            and attempt number'''
        return self.filter(
            question_paper_id=questionpaper_id,
            attempt_number=attempt_number, status=status
        ).count()

    def get_question_statistics(self, questionpaper_id):
        ''' Return dict with question object as key and list as value
            The list contains two value, first the number of times a question
            was answered correctly, and second the number of times a question
            appeared in a quiz'''
        question_stats = {}
        questions_answered = self.get_all_questions_answered(questionpaper_id)
        questions_unanswered = self.get_all_questions_unanswered(questionpaper_id)
        questions_wrong_answered = self.get_all_questions_wrong_answered(questionpaper_id)
        questions = self.get_all_questions(questionpaper_id)
        all_questions = Question.objects.filter(
                id__in=set(questions),
                active=True
            ).order_by('type')
        for question in all_questions:
            question_stats[question] = [questions_answered[question.id],
                                            questions[question.id], questions_unanswered[question.id], questions_wrong_answered[question.id]]
        return question_stats

    def _get_answerpapers_for_quiz(self, questionpaper_id, status=False):
        if not status:
            return self.filter(question_paper_id=questionpaper_id)
        else:
            return self.filter(question_paper_id=questionpaper_id,
                               status="completed")

    def _get_answerpapers_users(self, answerpapers):
        return answerpapers.values_list('user', flat=True).distinct()

    def get_latest_attempts(self, questionpaper_id):
        papers = self._get_answerpapers_for_quiz(questionpaper_id)
        users = self._get_answerpapers_users(papers)
        latest_attempts = []
        for user in users:
            latest_attempts.append(self._get_latest_attempt(papers, user))
        return latest_attempts

    def _get_latest_attempt(self, answerpapers, user_id):
        return answerpapers.filter(
            user_id=user_id
        ).order_by('-attempt_number')[0]

    def get_user_last_attempt(self, questionpaper, user):
        attempts = self.filter(question_paper=questionpaper,
                               user=user).order_by('-attempt_number')
        if attempts:
            return attempts[0]

    def get_user_answerpapers(self, user):
        return self.filter(user=user)

    def get_total_attempt(self, questionpaper, user):
        return self.filter(question_paper=questionpaper, user=user).count()

    def get_users_for_questionpaper(self, questionpaper_id):
        return self._get_answerpapers_for_quiz(questionpaper_id, status=True)\
            .values("user__id", "user__first_name", "user__last_name")\
            .distinct()

    def get_user_all_attempts(self, questionpaper, user):
        return self.filter(question_paper=questionpaper, user=user)\
                            .order_by('-attempt_number')

    def get_user_data(self, user, questionpaper_id, attempt_number=None):
        if attempt_number is not None:
            papers = self.filter(user=user, question_paper_id=questionpaper_id,
                                 attempt_number=attempt_number)
        else:
            papers = self.filter(
                user=user, question_paper_id=questionpaper_id
            ).order_by("-attempt_number")
        data = {}
        profile = user.profile if hasattr(user, 'profile') else None
        data['user'] = user
        data['profile'] = profile
        data['papers'] = papers
        data['questionpaperid'] = questionpaper_id
        return data

    def get_user_best_of_attempts_marks(self, quiz, user_id):
        best_attempt = 0.0
        papers = self.filter(question_paper__quiz=quiz,
                             user=user_id).values("marks_obtained")
        if papers:
            best_attempt = max([marks["marks_obtained"] for marks in papers])
        return best_attempt


class AnswerPaper(models.Model):
    """A answer paper for a student -- one per student typically.
    """
    # The user taking this question paper.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    questions = models.ManyToManyField(Question, related_name='questions')

    # The Quiz to which this question paper is attached to.
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)

    # The attempt number for the question paper.
    attempt_number = models.IntegerField()

    # The time when this paper was started by the user.
    start_time = models.DateTimeField()

    # The time when this paper was ended by the user.
    end_time = models.DateTimeField()

    # User's IP which is logged.
    user_ip = models.CharField(max_length=15)

    # All the submitted answers.
    answers = models.ManyToManyField(Answer)

    # Teacher comments on the question paper.
    comments = models.TextField()

    # Total marks earned by the student in this paper.
    marks_obtained = models.FloatField(null=True, default=0.0)

    # Marks percent scored by the user
    percent = models.FloatField(null=True, default=0.0)

    # Result of the quiz, True if student passes the exam.
    passed = models.NullBooleanField()

    instruction_read = models.BooleanField(default=False)

    # Status of the quiz attempt
    status = models.CharField(
        max_length=20, choices=test_status,
        default='inprogress'
    )

    objects = AnswerPaperManager()

    def truncate(self, number, digits):
        stepper = 10.0 ** digits
        return float(math.trunc(stepper * number) / stepper)

    def add_answer_key(self, question_id, answer_key="NA", status="0", time_spent=0):
        current_question = Question.objects.get(id=question_id)
        user_answer = self.answers.filter(question=current_question).first()
        expected_answer = current_question.get_right_answer()

        if user_answer is None:
            user_answer = Answer(question=current_question, answer=answer_key, time_spent=time_spent)
            user_answer.save()
            self.answers.add(user_answer)

        else:
            user_answer.set_answer(answer_key)
            user_answer.set_status(status)
            user_answer.set_time_spent(time_spent)
            if status == "2" or status == "4":
                if current_question.type == "integer":
                    try:
                        expected_answer = float(expected_answer)
                        answer_key = float(answer_key)

                        if expected_answer == round(answer_key, 2) or expected_answer == self.truncate(answer_key, 2):
                            user_answer.mark_answer(True)
                            user_answer.set_marks(current_question.points)

                        else:
                            user_answer.mark_answer(False)
                            user_answer.set_marks(current_question.negative_point)
                    except (TypeError, ValueError):
                        user_answer.mark_answer(False)
                        user_answer.set_marks(current_question.negative_point)

                else:
                    if expected_answer == answer_key:
                        user_answer.mark_answer(True)
                        user_answer.set_marks(current_question.points)
                    else:
                        user_answer.mark_answer(False)
                        user_answer.set_marks(current_question.negative_point)
            elif status == "3":
                user_answer.mark_answer(False)
                user_answer.set_marks(0)

            user_answer.save()

    def save_unanswered(self, question_id, time_spent=0):
        current_question = Question.objects.get(id=question_id)
        user_answer = self.answers.filter(question=current_question).first()
        if user_answer.status == "0":
            user_answer.set_status("1")
        user_answer.set_time_spent(time_spent)
        user_answer.save()

    def clear_answer(self, question_id):
        """ clear previous answers and mark answer as unanswered, status='1' """
        current_question = Question.objects.get(id=question_id)
        user_answer = self.answers.filter(question=current_question).first()
        user_answer.set_status("1")
        user_answer.set_marks("0")
        user_answer.set_answer("NA")
        user_answer.mark_answer(False)
        user_answer.save()

    def get_current_question_num(self, question_id):
        for num in range(0, self.questions.all().count()):
            if question_id == self.questions.all()[num].id:
                return num

    def get_questions_section_wise(self, section=None, question_subject=None):
        if section:
            if question_subject:
                return self.questions.filter(question_section=section).filter(subject=question_subject)
            return self.questions.filter(question_section=section)
        return self.questions.all()

    def next_section_id(self, section):
        for sec, startId in six.iteritems(self.get_question_section()):
            if sec == section:
                return startId[0]['startId']

    def time_left(self):
        """Return the time remaining for the user in seconds."""
        dt = timezone.now() - self.start_time
        try:
            mins = dt.total_seconds() / 60.0
        except AttributeError:
            # total_seconds is new in Python 2.7. :(
            mins = (dt.seconds + dt.days * 24 * 3600) / 60.0

        total = self.question_paper.quiz.duration

        remain = max(total - mins, 0)
        return remain

    def time_left_hour(self):
        """Return the time remaining for the user in seconds."""
        dt = timezone.now() - self.start_time
        try:
            secs = dt.total_seconds()
        except AttributeError:
            # total_seconds is new in Python 2.7. :(
            secs = dt.seconds + dt.days * 24 * 3600.0
        total = self.question_paper.quiz.duration * 60.0
        remain = max(total - secs, 0)
        return int(remain)

    def get_attempt_count(self):
        return self.answers.filter(Q(status='2') | Q(status="4")).count()
        # count = 0
        # marks = 0
        # for answer in self.answers.all():
        #     marks += answer.marks
        #     if answer.status == "2" or answer.status == "4":
        #         count += 1
        # self.marks_obtained = float(marks)
        # self.save()
        # return count

    def get_correct_answer_num(self):
        return self.answers.filter(Q(correct=True) & (Q(status="2") | Q(status="4"))).count()
        
        # count = 0
        # for answer in self.answers.all():
        #     if answer.correct:
        #         count += 1
        # return count

    def _get_attempt_count_by_subject(self, subject):
        return self.answers.filter(Q(question__subject=subject) & (Q(status="2") | Q(status="4"))).count()

        # count = 0
        # marks = 0
        # for answer in self.answers.filter(question__subject = subject):
        #     marks += answer.marks
        #     if answer.status == "2" or answer.status == "4":
        #         count += 1
        # self.marks_obtained = float(marks)
        # self.save()
        # return count

    def _get_attempt_count_by_type(self, question_type):
        return self.answers.filter(Q(question__type=question_type) & (Q(status="2") | Q(status="4"))).count()

        # count = 0
        # marks = 0
        # for answer in self.answers.filter(question__type = question_type):
        #     marks += answer.marks
        #     if answer.status == "2" or answer.status == "4":
        #         count += 1
        # self.marks_obtained = float(marks)
        # self.save()
        # return count

    def get_attempt_count_in_mcq(self):
        return self._get_attempt_count_by_type(question_type="mcq")

    def get_attempt_count_in_integer(self):
        return self._get_attempt_count_by_type(question_type="integer")

    def _get_correct_answer_num_by_subject(self, subject):
        return self.answers.filter(Q(question__subject=subject) & Q(correct=True)).count()
        

    def _get_correct_answer_num_by_type(self, question_type):
        return self.answers.filter(Q(question__type=question_type) & Q(correct=True) & (Q(status="2") | Q(status="4"))).count()

        # count = 0
        # for answer in self.answers.filter(question__type=question_type):
        #     if answer.correct:
        #         count += 1
        # return count

    def get_correct_answer_number_in_mcq(self):
        return self._get_correct_answer_num_by_type(question_type="mcq")

    def get_correct_answer_number_in_integer(self):
        return self._get_correct_answer_num_by_type(question_type="integer")


    def _get_wrong_answer_num_by_subject(self, subject):
        return self._get_attempt_count_by_subject(subject) - self._get_correct_answer_num_by_subject(subject)

    def get_wrong_answer_num_in_mcq(self):
        return self.get_attempt_count_in_mcq() - self.get_correct_answer_number_in_mcq()

    def get_wrong_answer_num_in_integer(self):
        return self.get_attempt_count_in_integer() - self.get_correct_answer_number_in_integer()
    

    def get_wrong_answer_num(self):
        return self.get_attempt_count() - self.get_correct_answer_num()

    def _get_marks_obtained_by_subject(self, subject):
        """Updates the total marks earned by student for this paper."""
        marks_by_subject = Sum('answers__marks', filter=Q(id=self.pk) & Q(answers__question__subject=subject))
        marks_dict = AnswerPaper.objects.aggregate(marks_by_subject=marks_by_subject)
        return marks_dict.get('marks_by_subject')
        # marks = 0
        # marks_dict =  self.answers.aggregate(Sum('marks'))
        # for question in self.questions.filter(subject=subject):
        #     marks_list = [a.marks
        #                   for a in self.answers.filter(question=question)]
        #     max_marks = max(marks_list) if marks_list else 0.0
        #     marks += max_marks
        # return marks

    def _get_marks_obtained_by_type(self, question_type):
        """Updates the total marks earned by student for this paper."""
        marks_by_type = Sum('answers__marks', filter=Q(id=self.pk) & Q(answers__question__type=question_type))
        marks_dict = AnswerPaper.objects.aggregate(marks_by_type=marks_by_type)
        return marks_dict.get('marks_by_type')
        # marks = 0
        # for question in self.questions.filter(type=question_type):
        #     marks_list = [a.marks
        #                   for a in self.answers.filter(question=question)]
        #     max_marks = max(marks_list) if marks_list else 0.0
        #     marks += max_marks
        # return marks

    def get_marks_obtained_in_integer(self):
        return self._get_marks_obtained_by_type(question_type="integer")

    def get_marks_obtained_in_mcq(self):
        return self._get_marks_obtained_by_type(question_type="mcq")

    def get_attempt_count_in_physics(self):
        return self._get_attempt_count_by_subject(subject="physics")

    def get_attempt_count_in_chemistry(self):
        return self._get_attempt_count_by_subject(subject="chemistry")

    def get_attempt_count_in_maths(self):
        return self._get_attempt_count_by_subject(subject="mathematics")

    def get_correct_answer_num_in_physics(self):
        return self._get_correct_answer_num_by_subject(subject="physics")

    def get_correct_answer_num_in_chemistry(self):
        return self._get_correct_answer_num_by_subject(subject="chemistry")

    def get_correct_answer_num_in_maths(self):
        return self._get_correct_answer_num_by_subject(subject="mathematics")

    def get_wrong_answer_num_in_physics(self):
        return self._get_wrong_answer_num_by_subject(subject="physics")
    
    def get_wrong_answer_num_in_chemistry(self):
        return self._get_wrong_answer_num_by_subject(subject="chemistry")

    def get_wrong_answer_num_in_maths(self):
        return self._get_wrong_answer_num_by_subject(subject="mathematics")

    def get_marks_obtained_in_physics(self):
        return self._get_marks_obtained_by_subject("physics")

    def get_marks_obtained_in_chemistry(self):
        return self._get_marks_obtained_by_subject("chemistry")

    def get_marks_obtained_in_mathematics(self):
        return self._get_marks_obtained_by_subject("mathematics")

    def get_marks_obtained(self):
        marks_total = Sum('answers__marks', filter=Q(id=self.pk))
        marks_dict = AnswerPaper.objects.aggregate(marks_total=marks_total)
        return marks_dict.get('marks_total')

    def _update_marks_obtained(self):
        """Updates the total marks earned by student for this paper."""
        marks_obtained = Sum('answers__marks', filter=Q(id=self.pk) & (Q(answers__status="2") | Q(answers__status="4") ))
        marks_dict = AnswerPaper.objects.aggregate(marks_obtained=marks_obtained) 
        self.marks_obtained = marks_dict.get('marks_obtained')

    def _update_percent(self):
        """Updates the percent gained by the student for this paper."""
        total_marks = self.question_paper.total_marks
        if self.marks_obtained is not None:
            percent = self.marks_obtained/total_marks*100
            self.percent = round(percent, 2)

    def _update_passed(self):
        """
            Checks whether student passed or failed, as per the quiz
            passing criteria.
        """
        if self.percent is not None:
            if self.percent >= self.question_paper.quiz.pass_criteria:
                self.passed = True
            else:
                self.passed = False

    def _update_status(self, state):
        """ Sets status as inprogress or completed """
        self.status = state

    def update_marks(self, state='completed'):
        self._update_marks_obtained()
        self._update_percent()
        self._update_passed()
        self._update_status(state)
        self.save()

    def set_end_time(self, datetime):
        """ Sets end time """
        self.end_time = datetime
        self.save()

    def get_question_answers(self):
        """
            Return a dictionary with keys as questions and a list of the
            corresponding answers.
        """
        return zip(self.question_paper.fixed_questions.all().order_by('question_section'),
                           self.answers.all().order_by('question__id'))

    def get_question_section(self):
        """
            Returns dictionary with keys as question section and a list of corresponding questions
        :return:
        """
        q_s = {}
        for question in self.questions.all():
            section = question.subject[:4]+" "+question.question_section
            if section not in q_s:
                q_s[section] = [{"startId": question.id}]

        return q_s

    def get_questions(self):
        return self.questions.filter(active=True)

    def is_answer_correct(self, question_id):
        ''' Return marks of a question answered'''
        return self.answers.filter(question_id=question_id,
                                   correct=True).exists()

    def is_attempt_inprogress(self):
        if self.status == 'inprogress':
            return self.time_left() > 0
        return False

    def get_previous_answers(self, question):
        return self.answers.filter(question=question).order_by('-id')

    def validate_answer(self, user_answer, question):
        """
            Checks whether the answer submitted by the user is right or wrong.
            If right then returns correct = True, success and
            message = Correct answer.
            success is True for MCQ's and multiple correct choices because
            only one attempt are allowed for them.
            For code questions success is True only if the answer is correct.
        """

        result = {'success': False, 'error': ['Incorrect answer'],
                  'weight': 0.0, 'partial': 0, 'negative': -1}
        if user_answer is not None:
            if question.type == 'mcq' or question.type == 'paragraph' or question.type == 'match':
                expected_answer = question.get_test_case(correct=True).options
                if user_answer.strip() == expected_answer.strip():
                    result['success'] = True
                    result['error'] = ['Correct answer']
                    result['negative'] = 0

            elif question.type == 'mcc':
                expected_answers = []
                for opt in question.get_test_cases(correct=True):
                    expected_answers.append(opt.options)
                if set(user_answer) == set(expected_answers):
                    result['success'] = True
                    result['error'] = ['Correct answer']
                    result['negative'] = 0
                elif set(expected_answers) > set(user_answer):
                    result['partial'] = len(set(user_answer))
                    result['error'] = ['Partially Correct']
                    result['negative'] = 0
                else:
                    result['negative'] = -2

            elif question.type == 'integer':
                expected_answers = []
                for tc in question.get_test_cases():
                    expected_answers.append(int(tc.correct))
                if int(user_answer) in expected_answers:
                    result['success'] = True
                    result['error'] = ['Correct answer']
                else:
                    result['negative'] = 0

        return result

    def regrade(self, question_id):
        try:
            question = self.questions.get(id=question_id)
            msg = 'User: {0}; Quiz: {1}; Question: {2}.\n'.format(
                    self.user, self.question_paper.quiz.description, question)
        except Question.DoesNotExist:
            msg = 'User: {0}; Quiz: {1} Question id: {2}.\n'.format(
                self.user, self.question_paper.quiz.description,
                question_id
            )
            return False, msg + 'Question not in the answer paper.'
        user_answer = self.answers.filter(question=question).last()
        if not user_answer:
            return False, msg + 'Did not answer.'
        if question.type == 'mcc':
            try:
                answer = eval(user_answer.answer)
                if type(answer) is not list:
                    return False, msg + 'MCC answer not a list.'
            except Exception:
                return False, msg + 'MCC answer submission error'
        else:
            answer = user_answer.answer
        result = self.validate_answer(answer, question)
        user_answer.correct = result.get('success')
        user_answer.error = result.get('error')
        if result.get('success'):
            user_answer.marks = question.points
        else:
            user_answer.marks = result.get('negative')+result.get('partial')
        user_answer.save()
        self.update_marks('completed')
        return True, msg

    def __str__(self):
        u = self.user
        q = self.question_paper.quiz
        return u'AnswerPaper paper of {0} {1} for quiz {2}'\
               .format(u.first_name, u.last_name, q.description)

###############################################################################


# class TestCase(models.Model):
#     question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
#     type = models.CharField(max_length=24, choices=test_case_types, null=True, default="mcqtestcase")


# class McqTestCase(TestCase):
#     options = models.CharField(max_length=100, blank=True, null=False)
#     correct = models.BooleanField(default=False)

#     def get_field_value(self):
#         return {"test_case_type": "mcqtestcase",
#                 "options": self.options, "correct": self.correct}

#     def __str__(self):
#         return u'MCQ Testcase | Correct: {0}'.format(self.correct)


# class IntegerTestCase(TestCase):
#     correct = models.FloatField(default=None)

#     def get_field_value(self):
#         return {"test_case_type": "integertestcase", "correct": self.correct}

#     def __str__(self):
#         return u'Integer Testcase | Correct: {0}'.format(self.correct)
