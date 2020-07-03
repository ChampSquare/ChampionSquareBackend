from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
from champsquarebackend.models.fields import AutoSlugField
from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.loading import get_model
# Create your models here.

user = get_user_model()
Question = get_model('question', 'question')

class AbstractCategory(models.Model):
    """
        Used to store a group of quizzes with same attributes/purposes
        Like 'Recruitment Tests' category will have quizzes used for requirement

        The deployment will create at lest one group named 'All' to which all tests
        will be part and can be changed by creating different categories.
    """

    name = models.CharField(_('Name'), max_length=128, unique=True, db_index=True)
    description = RichTextUploadingField(verbose_name=_("Description"), null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='categories', 
                              blank=True, null=True)
    slug = AutoSlugField(_('Slug'), max_length=128, unique=True,
                         populate_from='name')
    is_public = models.BooleanField(_("Is Public"), default=False, db_index=True)
    
    class Meta:
        abstract = True
        app_label = 'quiz'
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class AbstractQuiz(TimestampedModel, ModelWithMetadata):
    """
        Model for quiz, think of it like an exam event in real world
    """
    category = models.ForeignKey('quiz.Category', related_name='quiz_category', 
                                 blank=True, null=True,
                                 on_delete=models.CASCADE)
    questionpaper = models.OneToOneField('quiz.QuestionPaper', verbose_name='questionpaper',
                                blank=True, null=True, on_delete=models.PROTECT,
                                help_text='Questionpaper which will be given to user taking this quiz')
    name = models.CharField(_('name'), max_length=128, help_text="Name of quiz")
    # will create url to access the quiz
    slug = AutoSlugField(_('slug'), max_length=128, unique=True,
                         populate_from='name')

    start_date_time = models.DateTimeField(_("Start date-time of quiz"),
                                           default=timezone.now,
                                           help_text="Date-time from which this quiz will be active")

    # if set, quiz can't be started after that
    end_date_time = models.DateTimeField(_("End date-time of quiz"),
                                         null=True, blank=True,
                                         help_text="Date-time after which this quiz will be deactivated automatically")                               
    # this is always in minutes
    duration = models.PositiveIntegerField(_("Duration of quiz"), default=60,
                                            help_text="Duration of quiz in minutes")

    # total marks of quiz, this will be auto filled based on
    # individual marks of questions appeared in exam, will not appear
    # in forms
    total_marks = models.FloatField(default=0.0)

    # description of quiz, can be blank
    description = models.TextField(_('description'), blank=True)

    # instructions of quiz
    instructions = RichTextUploadingField(verbose_name=_('instructions of quiz'), blank=True, null=True,
                                                help_text="Instructions to show users before they take exam")

    # admin must publish the quiz for others to access after creating it
    # can be unpublished once it is complete
    is_published = models.BooleanField(_("Publish"), default=False,
                                       help_text="Publish the quiz, won't be accessible if you don't publish it")

    # Public test will appear in Quiz Catalogue and can be taken by anyone
    # who has access to it
    is_public = models.BooleanField(_("Public"), default=False,
                                help_text="Public quizzes will appear in quiz catalogue and can be taken by users registered on site")

    # is multiple attempts allowed?
    # default is false,
    # true -> user can take same quiz again and again even after submitting
    multiple_attempts_allowed = models.BooleanField(default=False,
                                                    help_text='Is user allowed to attempt same quiz multiple time?')

    # is user allowed to view his answerpaper report after submitting quiz
    view_answerpaper = models.BooleanField(default=False,
                                           help_text='Is user allowed to view his test report after he submits the test!')

    class Meta:
        abstract = True
        app_label = 'quiz'
        ordering = ['name']
        verbose_name = _('Quiz')
        verbose_name_plural = _("Quizzes")

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


class AbstractQuestionPaper(TimestampedModel, ModelWithMetadata):
    """ QuestionPaper stores the details of the quiestions """

    # Question paper belongs to a particular Quiz
    # Each question paper is unique to all students appearing in quiz
    # although oreder can be changed by re-shuffling of questions for each user

    questions = models.ManyToManyField(Question, 
                                       verbose_name=_('Questions'),
                                       related_name='questions')
    # if true, questions will appear in random orders for each users
    shuffle_questions = models.BooleanField(default=False)
    # total number of questions that will appear in exam
    # will be autofilled
    total_questions = models.IntegerField(default=0)

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _('QuestionPaper')
        verbose_name_plural = _("QuestionPapers")

    def _update_total_questions(self):
        """ Update number of questions """
        self.total_questions = self.questions.count()

    def _update_total_marks(self):
        """ Update total marks of quiz """
        pass


class AbstractAnswerPaper(TimestampedModel, ModelWithMetadata):
    """
        An answer paper for a student -- one per student typically
    """
    # the user taking this exam
    users = models.ForeignKey(user, on_delete=models.CASCADE, related_name='user')
    
    # quiz to which answerpaper is associated
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.PROTECT)

    # questionpaper to which this AnswerPaper belongs
    question_paper = models.ForeignKey('quiz.QuestionPaper', on_delete=models.CASCADE)

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

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _('AnswerPaper')
        verbose_name_plural = _("AnswerPapers")