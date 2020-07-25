from decimal import Decimal as D

from django import http
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from champsquarebackend.core.loading import get_class, get_model
from champsquarebackend.core.compat import get_user_model

from . import exceptions

QuizCreateSessionData = get_class(
    'dashboard.quiz.utils', 'QuizCreateSessionData')

Category = get_model('quiz', 'category')
Question = get_model('question', 'question')
Quiz = get_model('quiz', 'quiz')

User = get_user_model()



class QuizCreateSessionMixin(object):
    """
    Mixin to provide common functionality shared between quiz create/update views.

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

    def dispatch(self, request, *args, **kwargs):
        # Assign the quiz create session manager so it's available in all quiz create/update
        # views.
        self.quiz_create_session = QuizCreateSessionData(request)

        # Enforce any pre-conditions for the view.
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

    def check_category_exists(self, request):
        if not Category.objects.all().count() > 0:
            raise exceptions.FailedPreCondition(
                url=reverse('dashboard:quiz-category-create'),
                message=_(
                    "You need to add at least one category to create quiz")
            )
