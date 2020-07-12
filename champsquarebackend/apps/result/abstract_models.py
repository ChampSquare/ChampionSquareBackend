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
# Create your models here.

User = get_user_model()


class AbstractResult(ModelWithMetadata):
    participant = models.OneToOneField('participate.Participate',
                                       related_name='result',
                                       on_delete=models.PROTECT,
                                       verbose_name=_('Participant'))

    marks = models.FloatField('Total Marks obtained', default=0.0)
    num_total_questions = models.IntegerField('Total Questions', default=0)
    num_correct_answers = models.IntegerField('Total correct answers', default=0)
    num_wrong_answers = models.IntegerField('Total correct answers', default=0)

    class Meta:
        abstract = True
        app_label = 'result'
        ordering = ['-marks']
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def __str__(self):
        return  'Result of user: %s ' % self.participant.full_name

    def get_quiz_total_marks(self):
        """Full marks of paper"""
        return self.participant.quiz.total_marks

    def get_right_answer_list(self):
        return self.participant.answerpaper.answers.filter()

    @property
    def get_marks_obtained(self):
        return self.marks