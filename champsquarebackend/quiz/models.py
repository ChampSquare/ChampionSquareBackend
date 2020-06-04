from django.db import models
from django.utils.translation import gettext_lazy as _

# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.core.models import TimestampedModel, ModelWithMetadata

# Create your models here.

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
    description = RichTextUploadingField()
    subject = models.ForeignKey(Subject, null=True, blank=True,
                                on_delete=models.SET_NULL, 
                                related_name='subjects', verbose_name=_('subjects'))
    topic = models.ForeignKey(Topic, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='topics', verbose_name=_('topic'))
    question_type = models.CharField(_('type of question'), max_length=50, 
                                        default='mcq', choices=QUESTION_TYPES)
    answer_options = models.ManyToManyField(AnswerOptions, verbose_name=_('Answer Options'))
    # inactive question won't appear in test
    active = models.BooleanField(_('question active?'), default=True)
    points = models.FloatField(_('points that each question carry'), default=4.0)
    negative_points = models.FloatField(_('negative points on wrong answer'), default=0.0)
    difficulty_level = models.CharField(_('difficulty level of question'), max_length=20, blank=True,
                                            null=True, choices=DIFFICULTY_LEVEL)
    solution = RichTextUploadingField(_('Solution of question'), blank=True, null=True)
    # tags for the Question
    # tags = TaggableManager(blank=True)


    def __str__(self) -> str:
        return '{0} : {1} : {2}'.format(self.id, self.subject, self.question_type)
    


