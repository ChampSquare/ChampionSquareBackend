import logging
import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.signing import BadSignature, Signer
from django.utils.crypto import constant_time_compare
from django.utils.timezone import now

# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
from champsquarebackend.models.fields import AutoSlugField
from champsquarebackend.core.compat import get_user_model

logger = logging.getLogger('champsquarebackend.participate')
User = get_user_model()

class AbstractParticipate(TimestampedModel, ModelWithMetadata):
    """
        This model mocks the event of user taking an exam 
    """
    number = models.UUIDField(
        _("Participation number"), default=uuid.uuid4, db_index=True, unique=True)
    # this tracks the site from which test participation happened
    site = models.ForeignKey(
        'sites.Site', verbose_name=_("Site"), null=True,
        on_delete=models.SET_NULL)
    quiz = models.ForeignKey(
        'quiz.Quiz', related_name='participants', verbose_name=_('Quiz'), on_delete=models.PROTECT)
    answerpaper = models.OneToOneField('quiz.AnswerPaper', verbose_name=_('AnswerPaper'),
                                        blank=True, null=True,
                                        on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, blank=True, null=True,
        verbose_name=_("User"), on_delete=models.SET_NULL)

    # the time after which paper can be started
    start_time = models.DateTimeField(_('Start time of paper'), blank=True, null=True)

    # the time after which paper can't be started
    end_time = models.DateTimeField(_('End time of paper'), blank=True, null=True)

    # user's ip address from which the exam was started
    # this will be set at start time
    user_ip = models.GenericIPAddressField(_('IP address of user'), blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'participate'
        ordering = ['-created_at']
        verbose_name = _('Participate')
        verbose_name_plural = _('Participates')

    def __str__(self):
        return "#%s" %(self.number)

    def verification_hash(self):
        signer = Signer(salt='champsquarebackend.apps.participate.Participate')
        return signer.sign(self.number)

    def check_verification_hash(self, hash_to_check):
        """
        Checks the received verification hash against this participation number.
        Returns False if the verification failed, True otherwise.
        """
        signer = Signer(salt='champsquarebackend.apps.participate.Participate')
        try:
            signed_number = signer.unsign(hash_to_check)
        except BadSignatire:
            return False

        return constant_time_compare(signed_number, self.number)

    @property
    def email(self):
        return self.user.email

    @property
    def full_name(self):
        if self.user.first_name:
            return self.user.get_full_name()
        return self.email

    def set_start_time(self, time):
        """ Set start time, do this after user finishes reading instruction"""
        self.start_time = time

    def get_webcam_video(self):
        if self.videos is not None:
            return self.videos.filter(Q(type="webcam") & Q(is_processed=True)).first()
        return None

    def get_screen_video(self):
        if self.videos is not None:
            return self.videos.filter(Q(type="screen") & Q(is_processed=True)).first()
        return None

    @property
    def has_taken_quiz(self):
        """checks whether user has taken test or not"""
        return hasattr(self, 'answerpapers') and \
             self.answerpapers is not None and \
                 self.answerpapers.count() > 0

    @property
    def get_start_time(self):
        if self.start_time is not None:
            return self.start_time
        return self.created_at

    @property
    def get_end_time(self):
        if self.end_time is not None:
            return self.end_time
        return self.quiz.end_date_time
