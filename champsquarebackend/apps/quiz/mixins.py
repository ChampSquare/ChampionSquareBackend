from decimal import Decimal as D

from django import http
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404


from champsquarebackend.core.loading import get_class, get_model
from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.utils import get_ip_address

from . import exceptions

QuizCreateSessionData = get_class(
    'dashboard.quiz.utils', 'QuizCreateSessionData')

Category = get_model('quiz', 'category')
Question = get_model('question', 'question')
Quiz = get_model('quiz', 'quiz')
Participant = get_model('participate', 'participant')
ParticipantCreator = get_class('participate.utils', 'ParticipantCreator')


User = get_user_model()

class QuizConditionsMixin(object):
    """
    Mixin to provide common functionality shared between quiz views.

    All quiz create/update views subclass this mixin. It ensures that all relevant
    quiz create/update information is available in the template context.
    """

    # A pre-condition is a condition that MUST be met in order for a view
    # to be available. If it isn't then the admin should be redirected
    # to a view *earlier* in the chain.
    # pre_conditions is a list of method names that get executed before the
    # normal flow of the view. Each method should check some condition has been
    # met. If not, then an exception is raised that indicates the URL the
    # admin will be redirected to.

    pre_conditions = None

    # A *skip* condition is a condition that MUST NOT be met in order for a
    # view to be available. If the condition is met, this means the view MUST
    # be skipped and the customer should be redirected to a view *later* in
    # the chain.
    # Skip conditions work similar to pre-conditions, and get evaluated after
    # pre-conditions have been evaluated.
    skip_conditions = None

    quiz = None
    participant = None
    answerpaper = None


    def dispatch(self, request, *args, **kwargs):
        # Assign the quiz create session manager so it's available in all quiz create/update
        # views.
        # Enforce any pre-conditions for the view.
        self.quiz = self.get_quiz()
        self.participant = self.get_participant()
        self.answerpaper = self.get_answerpaper()
        try:
            self.check_pre_conditions(request)
        except exceptions.FailedPreCondition as e:
            for message in e.messages:
                messages.warning(request, message)
            return http.HttpResponseRedirect(e.url)

        # Check if this view should be skipped
        try:
            self.check_skip_conditions(request)
        except exceptions.PassedSkipCondition as e:
            return http.HttpResponseRedirect(e.url)

        return super().dispatch(
            request, *args, **kwargs)

    def get_quiz(self):
        if self.quiz is None:
            self.quiz = get_object_or_404(Quiz, id=self.kwargs['pk'])
        return self.quiz

    def get_participant(self):
        if self.participant is None:
            self.participant = get_object_or_404(Participant, id=self.kwargs['number'], quiz=self.kwargs['pk'])
        return self.participant

    def get_answerpaper(self):
        if self.answerpaper is None:
            creator = ParticipantCreator()
            self.answerpaper = creator.start_quiz(quiz=self.get_quiz(),
                                                   participant=self.get_participant(),
                                                   request=self.request)
        return self.answerpaper

    def check_pre_conditions(self, request):
        pre_conditions = self.get_pre_conditions(request)
        for method_name in pre_conditions:
            if not hasattr(self, method_name):
                raise ImproperlyConfigured(
                    "There is no method '%s' to call as a pre-condition" % (
                        method_name))
            getattr(self, method_name)(request)

    def get_pre_conditions(self, request):
        """
        Return the pre-condition method names to run for this view
        """
        if self.pre_conditions is None:
            return []
        return self.pre_conditions

    def check_skip_conditions(self, request):
        skip_conditions = self.get_skip_conditions(request)
        for method_name in skip_conditions:
            if not hasattr(self, method_name):
                raise ImproperlyConfigured(
                    "There is no method '%s' to call as a skip-condition" % (
                        method_name))
            getattr(self, method_name)(request)

    def get_skip_conditions(self, request):
        """
        Return the skip-condition method names to run for this view
        """
        if self.skip_conditions is None:
            return []
        return self.skip_conditions

    # Re-usable pre-condition validators

    def is_participant(self, request):
        """
            check participant belongs to quiz participant list or not
        """
        if self.participant.user not in self.quiz.users.all():
            raise exceptions.FailedPreCondition(
                url=reverse('quiz:error'),
                message=_(
                    "You are not allowed to take this quiz")
            )

    def can_take_new(self, request):
        """
            check if participant has already taken the exam
            and allow/disallow based on whether multiple attempt is
            enabled or not.
        """
        if self.participant.has_taken_quiz and \
                not self.participant.multiple_attempts_allowed and \
                    self.answerpaper.is_new():
            self.answerpaper.delete()
            raise exceptions.FailedPreCondition(
                url=reverse('quiz:error'),
                message=_(
                    "You have already taken this test and not allowed to take it again!")
            )

    def check_ip_restriction(self, request):
        """
            check for ip restriction when user resumes the test
        """
        ip_address = get_ip_address(request)
        if not self.answerpaper.is_new() and \
            self.participant.ip_restriction and \
                self.answerpaper.user_ip != ip_address:
            raise exceptions.FailedPreCondition(
                url=reverse('quiz:error'),
                message=_(
                    "Ip address changed!\nYou are not allowed to resume test from new ip address %s")
            )


    def can_resume(self, request):
        """
            If Internet is broken/disconnected user should be able to resume from 
            within 15 minutes, if it exceeds time the user will not be able to 
            resume exam, they have to start from beginning
        """
        if not self.answerpaper.is_new() and self.answerpaper.can_resume():
            # delete the old answerpaper first
            self.answerpaper.delete()
            raise exceptions.FailedPreCondition(
                url=self.participant.get_absolute_url(),
                message=_(
                    "You were disconnected for more than %s minutes,"
                    "you will have to start from beginning" % (self.participant.resume_interval))
            )


