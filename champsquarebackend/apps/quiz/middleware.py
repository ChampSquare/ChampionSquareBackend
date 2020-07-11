from django.conf import settings
from django.contrib import messages
from django.core.signing import BadSignature, Signer
from django.utils.functional import SimpleLazyObject, empty
from django.utils.translation import gettext_lazy as _

from champsquarebackend.core.loading import get_class, get_model

AnswerPaper = get_model('quiz', 'AnswerPaper')
# Selector = get_class('partner.strategy', 'Selector')

# selector = Selector()


class AnswerPaperMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Keep track of cookies that need to be deleted (which can only be done
        # when we're processing the response instance).
        request.cookies_to_delete = []

        # We lazily load the answerpaper so use a private variable to hold the
        # cached instance.
        request._answerpaper_cache = None

        def load_full_answerpaper():
            """
            Return the answerpaper after applying offers.
            """
            answerpaper = self.get_answerpaper(request)
            
            # self.apply_offers_to_answerpaper(request, answerpaper)

            return answerpaper

        def load_answerpaper_hash():
            """
            Load the answerpaper and return the answerpaper hash

            Note that we don't apply offers or check that every line has a
            stockrecord here.
            """
            answerpaper = self.get_answerpaper(request)
            if answerpaper.id:
                return self.get_answerpaper_hash(answerpaper.id)

        # Use Django's SimpleLazyObject to only perform the loading work
        # when the attribute is accessed.
        request.answerpaper = SimpleLazyObject(load_full_answerpaper)
        request.answerpaper_hash = SimpleLazyObject(load_answerpaper_hash)

        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        # Delete any surplus cookies
        cookies_to_delete = getattr(request, 'cookies_to_delete', [])
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)

        if not hasattr(request, 'answerpaper'):
            return response

        # If the answerpaper was never initialized we can safely return
        if (isinstance(request.answerpaper, SimpleLazyObject)
                and request.answerpaper._wrapped is empty):
            return response

        cookie_key = self.get_cookie_key(request)
        # Check if we need to set a cookie. If the cookies is already available
        # but is set in the cookies_to_delete list then we need to re-set it.
        has_answerpaper_cookie = (
            cookie_key in request.COOKIES
            and cookie_key not in cookies_to_delete)

        return response

    def get_cookie_key(self, request):
        """
        Returns the cookie name to use for storing a cookie answerpaper.

        The method serves as a useful hook in multi-site scenarios where
        different answerpapers might be needed.
        """
        return settings.SETTINGS_ANSWERPAPER_COOKIE_OPEN

    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            if response.context_data is None:
                response.context_data = {}
            if 'answerpaper' not in response.context_data:
                response.context_data['answerpaper'] = request.answerpaper
            else:
                # Occasionally, a view will want to pass an alternative answerpaper
                # to be rendered.  This can happen as part of checkout
                # processes where the submitted answerpaper is frozen when the
                # customer is redirected to another site (eg PayPal).  When the
                # customer returns and we want to show the order preview
                # template, we need to ensure that the frozen answerpaper gets
                # rendered (not request.answerpaper).  We still keep a reference to
                # the request answerpaper (just in case).
                response.context_data['request_answerpaper'] = request.answerpaper
        return response

    # Helper methods

    def get_answerpaper(self, request):
        """
        Return the open answerpaper for this request
        """
        if request._answerpaper_cache is not None:
            return request._answerpaper_cache

        num_answerpapers_merged = 0
        manager = AnswerPaper.open
        cookie_key = self.get_cookie_key(request)
        cookie_answerpaper = self.get_cookie_answerpaper(cookie_key, request, manager)

        if hasattr(request, 'user') and request.user.is_authenticated:
            # Signed-in user: if they have a cookie answerpaper too, it means
            # that they have just signed in and we need to merge their cookie
            # answerpaper into their user answerpaper, then delete the cookie.
            try:
                answerpaper, __ = manager.get_or_create(owner=request.user)
            except AnswerPaper.MultipleObjectsReturned:
                # Not sure quite how we end up here with multiple answerpapers.
                # We merge them and create a fresh one
                old_answerpapers = list(manager.filter(owner=request.user))
                answerpaper = old_answerpapers[0]
                for other_answerpaper in old_answerpapers[1:]:
                    self.merge_answerpapers(answerpaper, other_answerpaper)
                    num_answerpapers_merged += 1

            # Assign user onto answerpaper to prevent further SQL queries when
            # answerpaper.owner is accessed.
            answerpaper.owner = request.user

            if cookie_answerpaper:
                self.merge_answerpapers(answerpaper, cookie_answerpaper)
                num_answerpapers_merged += 1
                request.cookies_to_delete.append(cookie_key)

        elif cookie_answerpaper:
            # Anonymous user with a answerpaper tied to the cookie
            answerpaper = cookie_answerpaper
        else:
            # Anonymous user with no answerpaper - instantiate a new answerpaper
            # instance.  No need to save yet.
            answerpaper = AnswerPaper()

        # Cache answerpaper instance for the during of this request
        request._answerpaper_cache = answerpaper

        if num_answerpapers_merged > 0:
            messages.add_message(request, messages.WARNING,
                                 _("We have merged a answerpaper from a previous session. Its contents "
                                   "might have changed."))

        return answerpaper

    def merge_answerpapers(self, master, slave):
        """
        Merge one answerpaper into another.

        This is its own method to allow it to be overridden
        """
        master.merge(slave, add_quantities=False)

    def get_cookie_answerpaper(self, cookie_key, request, manager):
        """
        Looks for a answerpaper which is referenced by a cookie.

        If a cookie key is found with no matching answerpaper, then we add
        it to the list to be deleted.
        """
        answerpaper = None
        if cookie_key in request.COOKIES:
            answerpaper_hash = request.COOKIES[cookie_key]
            try:
                answerpaper_id = Signer().unsign(answerpaper_hash)
                answerpaper = AnswerPaper.objects.get(pk=answerpaper_id, owner=None,
                                            status=AnswerPaper.OPEN)
            except (BadSignature, AnswerPaper.DoesNotExist):
                request.cookies_to_delete.append(cookie_key)
        return answerpaper

    def apply_offers_to_answerpaper(self, request, answerpaper):
        if not answerpaper.is_empty:
            Applicator().apply(answerpaper, request.user, request)

    def get_answerpaper_hash(self, answerpaper_id):
        return Signer().sign(answerpaper_id)
