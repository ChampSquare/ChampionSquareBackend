from django.db import models
from django.utils.translation import gettext_lazy as _

# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
from champsquarebackend.models.fields import AutoSlugField


class AbstractSubject(models.Model):
    """
     Subject each question belongs to
    """
    name = models.CharField(_("name of subject"), max_length=50, unique=True)

    class Meta:
        abstract = True
        app_label = 'question'
        ordering = ['name']
        verbose_name = _('Subject')
        verbose_name_plural = _("Subjects")

    def __str__(self) -> str:
        return self.name

class AbstractTopic(models.Model):
    """
     Topic (belonging to subject) each question belongs to
    """
    name = models.CharField(_("name of topic"), max_length=100, unique=True)
    subject = models.ForeignKey('question.Subject', on_delete=models.CASCADE, verbose_name=_('Subject'))

    class Meta:
        abstract = True
        app_label = 'question'
        ordering = ['name']
        verbose_name = _('Topic')
        verbose_name_plural = _("Topics")
        unique_together = ('name', 'subject')

    def __str__(self) -> str:
        return '{0} : {1}'.format(self.subject, self.name)


class AbstractAnswerOptions(models.Model):
    """
        Options attached to each questions, depends on type of question
    """
    option = RichTextUploadingField(_('option field'))
    correct = models.BooleanField(_('Whether this option is correct or not'), default=False)

    class Meta:
        abstract = True
        app_label = 'question'
        ordering = ['id']
        verbose_name = _('AnswerOption')
        verbose_name_plural = _("AnswerOptions")

    def __str__(self) -> str:
        return '{0} : {1}'.format(self.option, self.correct)


class AbstractQuestion(TimestampedModel, ModelWithMetadata):
    """
        model for Question
    """

    description = RichTextUploadingField()
    subject = models.ForeignKey('question.Subject', null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='subjects', verbose_name=_('subjects'))
    topic = models.ForeignKey('question.Topic', null=True, blank=True,
                              on_delete=models.SET_NULL,
                              related_name='topics', verbose_name=_('topic'))

    QUESTION_TYPES = (
        (None, "Choose Question Type"),
        ("mcq", "Single Correct Choice"),
        ("mcc", "Multiple Correct Choices"),
        ("integer", "Answer in Integer"),
        ("paragraph", "Paragraph Type")
        )

    question_type = models.CharField(_('type of question'), max_length=50,
                                     default='mcq', choices=QUESTION_TYPES)
    # answer_options = models.ManyToManyField(AnswerOptions, verbose_name=_('Answer Options'))
    right_answer = models.CharField(_('right answer'), max_length=10, null=True, blank=True)
    # inactive question won't appear in test
    active = models.BooleanField(_('question active?'), default=True)
    points = models.FloatField(_('points that each question carry'), default=4.0)
    negative_points = models.FloatField(_('negative points on wrong answer'),
                                        default=0.0)
    DIFFICULTY_LEVEL = (
                (None, "Choose Difficulty Level"),
                ('easy', 'Easy'),
                ('medium', 'Medium'),
                ('hard', 'Hard')
                )
    difficulty_level = models.CharField(_('difficulty level of question'),
                                        max_length=20, blank=True,
                                        null=True, choices=DIFFICULTY_LEVEL)
    solution = RichTextUploadingField(_('Solution of question'), blank=True, null=True)
    # tags for the Question
    # tags = TaggableManager(blank=True)

    class Meta:
        abstract = True
        app_label = 'question'
        ordering = ['id']
        verbose_name = _('Question')
        verbose_name_plural = _("Questions")


    def __str__(self) -> str:
        return '{0} : {1} : {2}'.format(self.id, self.subject, self.question_type)
    
    @property
    def get_description(self):
        return self.description
