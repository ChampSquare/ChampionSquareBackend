import logging
import itertools

from django.db import models
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
        _("Participation number"), db_index=True, unique=True)
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

    # the time when paper was started by user
    start_time = models.DateTimeField(_('Start time of paper'), blank=True, null=True)

    # the time when paper was submitted by user
    end_time = models.DateTimeField(_('End time of paper'), blank=True, null=True)

    # user's ip address from which the exam was started
    # this will be set at start time
    user_ip = models.GenericIPAddressField(_('IP address of user'), blank=True, null=True)

    test_status_options = {
        'In-progress': ('created', 'on_permission_page' 'on_instruction', 'answering',),
        'Paused': ('Paused by Admin', 'Network Issue'),
        'Cancelled': ('Blocked by Admin', 'User Left'),
        'Completed': ('Submitted by User', 'Autosubmitted')
    }
    status = models.CharField(
        _('Status of Test'), max_length=32, blank=True)

    class Meta:
        abstract = True
        app_label = 'participate'
        ordering = ['-start_time']
        verbose_name = _('Participate')
        verbose_name_plural = _('Participates')

    def __str__(self):
        return "#%s" %(self.number)
    

    @classmethod
    def all_statuses_attr(cls):
        """
            Return all possible statuses for a participation
        """
        return list(cls.test_status_options.keys())

    def available_statues(self):
        """
            Return all possible statuses that this participation can move to
        """
        return list(itertools.chain(*list(self.test_status_options.values())))

    def set_status(self, new_status):
        """
        Set a new status for this participation

        If the requested status is not valid, then ``InvalidParticipationStatus`` is
        raised
        """
        if new_status == self.status:
            return
        
        old_status = self.status
        if new_status not in self.available_statues:
            raise exceptions.InvalidOrderStatus(
                _("'%(new_status)s' is not a valid status for order %(number)s"
                  " (current status: '%(status)s')")
                % {'new_status': new_status,
                   'number': self.number,
                   'status': self.status})

        self.status = new_status
        self.save()

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
        self.set_status('answering')



        



    