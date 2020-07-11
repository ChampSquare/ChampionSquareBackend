import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import PermissionDenied

# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
from champsquarebackend.models.fields import AutoSlugField
from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.loading import get_model
from . import exceptions
# Create your models here.

User = get_user_model()
Answer = get_model('quiz', 'answer')


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

    users = models.ManyToManyField(User, blank=True, related_name='users',
                                   verbose_name=_('Users'), default=1)

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

    def check_user_eligibility(self, user):
        """ 
            checks whether user is eligible to take this quiz or not,
            return: True, False
        """
        # a staff is always allowed to take quiz
        if user.is_staff:
            return True

        if hasattr(self, 'users') and user in self.users.all():
            if not self.multiple_attempts_allowed and self.has_user_taken_quiz(user):
                return False
        # todo: if user is not users list return False
        return True

    def has_user_taken_quiz(self, user):
        """
            checks whether given user has already take the quiz or not
        """
        return user in self.get_all_participants

    @property
    def has_questions(self):
        if not hasattr(self, 'questionpaper') or self.questionpaper is  None:
            return False
        return  self.questionpaper.get_questions_num > 0

    @property
    def get_all_participants(self):
        return self.participants.all()
        
    def can_be_taken(self, user):
        """
            checks if this quiz can be taken or not
        """
        if not self.has_questions:
            return False, 'reason: quiz has no question'
        
        if not self.check_user_eligibility(user):
            return False, 'reason: user has already taken the quiz and multi-attempt is not allowed for this quiz'

        return user.is_staff or self.is_published, 'reason: quiz is not published'


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

    questions = models.ManyToManyField(
        'question.Question', related_name='includes',
        verbose_name=_('Questions'))
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

    def add_question(self, question, display_order=None):
        """ Add question to questionpaper

        When adding a question that is already in the questionpaper, preven 
        re-adding it.

        If display_order is specified, update it.

        Default display_order for a new question in the questionpaper is 0;
        This puts the question at the top of the list
        """

        pass

    def get_all_questions(self):
        return self.questions.all()

    @property
    def get_questions_num(self):
        return self.get_all_questions().count()

    def get_all_subjects(self):
        """ returns list of all subjects in this questionpaper"""
        return list(self.questions.order_by().values_list('subject__name', flat=True).distinct())




class AbstractAnswerPaper(TimestampedModel, ModelWithMetadata):
    """
        An answer paper for a student -- one per student typically
    """
    # an unique identifer
    participant_number = models.UUIDField(default=uuid.uuid4, editable=False)   
    # quiz to which answerpaper is associated
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.PROTECT, related_name='answerpapers')
    
    # is trial, trail quizzes are one which are taken by staff members for debugging
    is_trial = models.BooleanField(_('Is trial?'), default=False)
    last_accessed = models.DateTimeField(_('Last Access Time'), null=True, blank=True)
    is_started = models.BooleanField(_('Is test started?'), default=False)
    is_submitted = models.BooleanField(_('Is Test Submitted?'), default=False)
    # the time when paper was started by user
    start_time = models.DateTimeField(_('Start time of paper'), blank=True, null=True)

    # the time by when paper must be submitted
    end_time = models.DateTimeField(_('End time of paper'), blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _('AnswerPaper')
        verbose_name_plural = _("AnswerPapers")
    
    @property
    def is_editable(self):
        """
            The answer paper can't be edited before and after the quiz
        """
        return self.is_started and not self.is_submitted

    def save(self, *args, **kwargs):
        self.last_accessed = timezone.now()
        super().save(*args, **kwargs) # Call the real save() method

    def add_answer_key(self, question_id, answer_key="NA", status="0", time_spent=0):
        current_question = self.quiz.questionpaper.questions.get(id=question_id)
        user_answer = self.answers.filter(question=current_question).first()
        expected_answer = current_question.get_right_answer

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
        current_question = self.question.objects.get(id=question_id)
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



class AbstractAnswer(ModelWithMetadata):
    """
     An answer submitted by user taking the exam
    """
    question = models.ForeignKey('question.Question', on_delete=models.PROTECT)
    answerpaper = models.ForeignKey('quiz.AnswerPaper', on_delete=models.PROTECT,
                                    related_name='answers', verbose_name=_('AnswerPaper'))
    answer = models.CharField(_("Answer"), max_length=128, blank=True)
    is_correct = models.BooleanField(
        _('Is this answer correct?'), default=False)
    points = models.FloatField(_("points gained"), default=0.0)
    ANSWER_STATUS_OPTIONS = (
        ('unattempted', 'Not Attempted'),
        ('skipped', 'Skipped'),
        ('answered', 'Answered'),
        ('marked', 'Marked For Review'),
        ('answered_and_marked', 'Answered & Marked For Review')
    )
    status = models.CharField(
        _('Status of Answer'),
        max_length=30, choices=ANSWER_STATUS_OPTIONS,
        default='unattempted')
    time_taken = models.FloatField(
        _('Time Taken'),
        default=0.0,
        help_text=_('Time Spent on particular question'))

    class Meta:
        abstract = True
        app_label = 'quiz'
        verbose_name = _('Answer submitted by user')
        verbose_name_plural = _('Answers submitted by user')
