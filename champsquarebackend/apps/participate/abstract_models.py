import logging
import uuid

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.signing import BadSignature, Signer
from django.utils.crypto import constant_time_compare
from django.utils.timezone import now
from django.urls import reverse


# from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
from champsquarebackend.models.fields import AutoSlugField
from champsquarebackend.core.compat import get_user_model

logger = logging.getLogger('champsquarebackend.participate')
User = get_user_model()

class AbstractParticipant(TimestampedModel, ModelWithMetadata):
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
    
    user = models.ForeignKey(
        User, blank=True, null=True,
        verbose_name=_("User"), on_delete=models.SET_NULL)

    start_date_time = models.DateTimeField(_("Start date-time of quiz"),
                                           default=now,
                                           help_text="Date-time from which this quiz will be active")

    # if set, quiz can't be started after that
    # local value will be preferred, the value must be before global value
    end_date_time = models.DateTimeField(_("End date-time of quiz"),
                        null=True, blank=True,
                        help_text=_("Date-time after which this quiz will be deactivated automatically"))
    # this is always in minutes
    # local value will be preferred
    duration = models.PositiveIntegerField(_("Duration of quiz"), default=60,
                    help_text="Duration of quiz in minutes")

    # admin must activate the quiz for others to access after creating it
    # can be deactivated once it is complete
    # global value will be preferred when False otherwise local value
    is_active = models.BooleanField(_("Is Published?"), default=True,
                    help_text="Only active user will be able to take quiz")

    # is multiple attempts allowed?
    # default is false,
    # true -> user can take same quiz again and again even after submitting
    multiple_attempts_allowed = models.BooleanField(_('Multiple Attempts Allowed?'),default=False,
                                    help_text=_('Is user allowed to attempt same quiz multiple time?'))

    # is user allowed to view his answerpaper report after submitting quiz
    view_answerpaper = models.BooleanField(_('Can see answer-paper?'), default=False,
                        help_text=_('Is user allowed to view his test report after he submits the test!'))

    # ip restriction, won't be able to resume exam if ip address changes
    ip_restriction = models.BooleanField(_('IP Restricted?'), default=False,
                        help_text=_('User will be only able to resume test from same ip if turned on!'))
    
    # allows to set an interval after which user won't be able to resume test
    resume_interval = models.PositiveIntegerField(_('Resume Interval'), default=15,
                        help_text=_('The time interval after which user will not be able to resume test'))

    video_monitoring_enabled = models.BooleanField(_('Video Monitoring Enabled?'), default=True,
                        help_text=_('Turn on/off video monitoring which includes webcam and screen recording'))

    # user's ip address from which the exam was started
    # this will be set at start time
    user_ip = models.GenericIPAddressField(_('IP address of user'), blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'participate'
        ordering = ['-created_at']
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')

    def __str__(self):
        return "#%s status: " %(self.full_name)

    def get_absolute_url(self):
        return reverse('quiz:quiz-take', kwargs={'pk': self.quiz.pk, 'number': self.id})

    def verification_hash(self):
        signer = Signer(salt='champsquarebackend.apps.participate.Participant')
        return signer.sign(self.number)

    def check_verification_hash(self, hash_to_check):
        """
        Checks the received verification hash against this participation number.
        Returns False if the verification failed, True otherwise.
        """
        signer = Signer(salt='champsquarebackend.apps.participate.Participant')
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

    @property
    def has_taken_quiz(self):
        """checks whether user has taken test or not"""
        return hasattr(self, 'answerpapers') and \
             self.answerpapers is not None and \
                 self.answerpapers.count() > 1

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
