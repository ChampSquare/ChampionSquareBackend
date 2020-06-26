from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
from champsquarebackend.models.fields import AutoSlugField
# Create your models here.

user = get_user_model()

QUESTION_TYPES = (
        (None, "Choose Question Type"),
        ("mcq", "Single Correct Choice"),
        ("mcc", "Multiple Correct Choices"),
        ("integer", "Answer in Integer"),
        ("paragraph", "Paragraph Type")
)

DIFFICULTY_LEVEL = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard')
)

class Subject(models.Model):
    """
     Subject each question belongs to
    """
    name = models.CharField(_("name of subject"), max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

class Topic(models.Model):
    """
     Topic (belonging to subject) each question belongs to
    """
    name = models.CharField(_("name of topic"), max_length=100, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('Subject'))

    class Meta:
        unique_together = ('name', 'subject')

    def __str__(self) -> str:
        return '{0} : {1}'.format(self.subject, self.name)


class AnswerOptions(models.Model):
    """
        Options attached to each questions, depends on type of question
    """
    option = RichTextUploadingField(_('option field'))
    correct = models.BooleanField(_('Whether this option is correct or not'), default=False)

    def __str__(self) -> str:
        return '{0} : {1}'.format(self.option, self.correct)
    

class Question(TimestampedModel, ModelWithMetadata):
    """
        model for Question
    """
    description = RichTextUploadingField()
    subject = models.ForeignKey(Subject, null=True, blank=True,
                                on_delete=models.SET_NULL, 
                                related_name='subjects', verbose_name=_('subjects'))
    topic = models.ForeignKey(Topic, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='topics', verbose_name=_('topic'))
    question_type = models.CharField(_('type of question'), max_length=50,
                                        default='mcq', choices=QUESTION_TYPES)
    # answer_options = models.ManyToManyField(AnswerOptions, verbose_name=_('Answer Options'))
    right_answer = models.CharField(_('right answer'), max_length=10, null=True, blank=True)
    # inactive question won't appear in test
    active = models.BooleanField(_('question active?'), default=True)
    points = models.FloatField(_('points that each question carry'), default=4.0)
    negative_points = models.FloatField(_('negative points on wrong answer'), 
                                        default=0.0)
    difficulty_level = models.CharField(_('difficulty level of question'), 
                                        max_length=20, blank=True,
                                        null=True, choices=DIFFICULTY_LEVEL)
    solution = RichTextUploadingField(_('Solution of question'), blank=True, null=True)
    # tags for the Question
    # tags = TaggableManager(blank=True)


    def __str__(self) -> str:
        return '{0} : {1} : {2}'.format(self.id, self.subject, self.question_type)


class Category(models.Model):
    """
        Used to store a group of quizzes with same attributes/purposes
        Like 'Recruitment Tests' category will have quizzes used for requirement

        The deployment will create at lest one group named 'All' to which all tests
        will be part and can be changed by creating different categories.
    """

    name = models.CharField(_('Name'), max_length=128)
    slug = AutoSlugField(_('Slug'), max_length=128, unique=True,
                         populate_from='name')

    def __str__(self):
        return self.name


class Quiz(TimestampedModel, ModelWithMetadata):
    """
        Model for quiz, think of it like an exam event in real world
    """
    category = models.ForeignKey(Category, related_name='quiz_category',
                                 on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=128)
    # will create url to access the quiz
    slug = AutoSlugField(_('slug'), max_length=128, unique=True,
                         populate_from='name')
    
    start_date_time = models.DateTimeField(_("Start date-time of quiz"),
                                           default=timezone.now)

    # if set, quiz can't be started after that
    end_date_time = models.DateTimeField(_("End date-time of quiz"),
                                         null=True, blank=True)                               
    # this is always in minutes
    duration = models.IntegerField(_("Duration of quiz"), default=60)

    # total marks of quiz, this will be auto filled based on
    # individual marks of questions appeared in exam
    total_marks = models.FloatField(default=0.0)

    # description of quiz, can be blank
    description = models.TextField(_('description'), blank=True)

    # instructions of quiz
    instructions = models.TextField(_('instructions of quiz'), blank=True)

    # admin must publish the quiz for others to access after creating it
    # can be unpublished once it is complete
    publish = models.BooleanField(default=False)

    # is multiple attempts allowed?
    # default is false,
    # true -> user can take same quiz again and again even after submitting
    multiple_attempts_allowed = models.BooleanField(default=False)

    # is user allowed to view his answerpaper report after submitting quiz
    view_answerpaper = models.BooleanField(default=False)

    # users who will be allowed to take test
    users = models.ManyToManyField(user, verbose_name=_('Users'),
                                help_text='User which will be allowed to take test')

    

    class Meta:
        verbose_name_plural = 'Quizzes'

    @property
    def get_time_to_start(self):
        """ Return the time remaining for quiz to start, 0 if already started"""
        dt = self.start_date_time - timezone.now()
        if dt <= 0:
            return 0
        try:
            mins = dt.total_seconds()/60.0
        except AttributeError:
            mins = (dt.seconds + dt.days * 24 * 3600) / 60.0
        return mins


    @property
    def is_started(self):
        return self.get_time_to_start <= 0

    def __str__(self):
        desc = self.description or 'Quiz'
        return '%s: on %s for %d minutes' % (desc, self.start_date_time,
                                             self.duration)


class QuestionPaper(TimestampedModel, ModelWithMetadata):
    """ QuestionPaper stores the details of the quiestions """

    # Question paper belongs to a particular Quiz
    # Each question paper is unique to all students appearing in quiz
    # although oreder can be changed by re-shuffling of questions for each user

    quiz = models.OneToOneField(Quiz, verbose_name='Quiz', on_delete=models.CASCADE,
                                help_text='Quiz to which this question paper belongs')
    questions = models.ManyToManyField(Question, verbose_name=_('Questions'), related_name='questions')
    # if true, questions will appear in different orders for users
    shuffle_question = models.BooleanField(default=False)
    # total number of questions that will appear in exam
    # will be autofilled
    total_questions = models.IntegerField(default=0)

    def _update_total_questions(self):
        """ Update number of questions """
        self.total_questions = self.questions.count()

    def _update_total_marks(self):
        """ Update total marks of quiz """


class AnswerPaper(TimestampedModel, ModelWithMetadata):
    """
        An answer paper for a student -- one per student typically
    """
    # the user taking this exam
    users = models.ForeignKey(user, on_delete=models.CASCADE, related_name='user')
    
    # quiz to which answerpaper is associated
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # questionpaper to which this AnswerPaper belongs
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)

    # the attempt number for the questionpaper
    # 0 -> User has not taken the exam
    # 1 -> User has taken the exam
    # > 1 -> Multiple attempt is enabled and user has taken multiple attempts
    attempt_number = models.IntegerField(_('Attempt number'))

    # the time when paper was started by user
    start_time = models.DateTimeField(_('Start time of paper'))

    # the time when paper was submitted by user
    end_time = models.DateTimeField(_('End time of paper'), blank=True, null=True)

    # last active time -> time when user was last active while
    # taking the exam, this will be used to write the logic
    # in case a network error happens during the exam
    last_active_time = models.DateTimeField(_('last active time of user'))

    # user's ip address from which the exam was started
    # this will be set at start time
    user_ip = models.GenericIPAddressField(_('IP address of user'))


    




    

