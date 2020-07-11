from django.apps import AppConfig as DjangoAppConfig
from django.core.exceptions import ImproperlyConfigured
from django.urls import URLPattern, reverse_lazy
from django.conf import settings

from .loading import feature_hidden

class AppConfigMixin(object):
    """
        Base app configuration mixin, used to extend
        :py:class: `django.apps.AppConfig`
        to also provide URL configurations and permissions
    """
    # Instance namespace for the URLs
    namespace = None
    login_url = None

    #: A name that allows the functionality within this app to be disabled
    hidable_feature_name = None

    #: Maps view names to lists of permissions. Expects tuples of
    #: lists as dictionary values. A list is a set of permissions that all
    #: need to be fullfilled (AND). Only one set of permssions has to be
    #: fulfilled (OR)
    #: If there's only one set of permissions, as a shortcut, you can
    #: just define one list
    permissions_map = {}

    #: Default permssion for nay view not in permissions_map
    default_permissions = None

    def __init__(self, app_name, app_module, namespace=None, **kwargs):
        """
        kwargs:
            namespace: optionally specify the URL instance namepace
        """

        app_config_attrs = [
            'name',
            'module',
            'apps',
            'label',
            'verbose_name',
            'path',
            'models_module',
            'models'
        ]

        # To ensure sub classes do not add kwargs that are used by
        # :py:class: `django.apps.AppConfig`
        clashing_kwargs = set(kwargs).intersection(app_config_attrs)
        if clashing_kwargs:
            raise ImproperlyConfigured(
                "Passes in kwargs can't be named the same as properties of "
                "AppConfig; clashing: %s" % ", ".join(clashing_kwargs))
        super().__init__(app_name, app_module)
        if namespace is not None:
            self.namespace = namespace
        # set all kwargs as object attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def get_urls(self):
        """
        Return the URL patterns for this app
        """
        return []

    def post_process_urls(self, urlpatterns):
        """
            Customize URL patterns

            This method allows decorators to be wrapped around an apps URL patterns.

            By default, this only allows custom decorators to be specified
            But can be overridden to do naything you want
        """
        # Test if this the URLs in the Application instance should be available.
        # If this feature is hidden then don't include the URLs
        if feature_hidden(self.hidable_feature_name):
            return []

        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                self.post_process_urls(pattern.url_patterns)

            if isinstance(pattern, URLPattern):
                # Apply the custom view decorator (if any) set for this class if this
                # is a URL Patterns
                decorator = self.get_url_decorator(pattern)
                if decorator:
                    pattern.callback = decorator(pattern.callback)

        return urlpatterns

    def get_permissions(self, url):
        """
            Return a list of permssions for a given URL name

            Args:
            url (str): A URL name (e.g., ``quiz:quiz``)

            Returns:
                list: A list of permssion strings
        """
        # url namespaced?
        if url is not None and ':' in url:
            view_name = url.split(':')[1]
        else:
            view_name = url
        return self.permissions_map.get(view_name, self.default_permissions)

    def get_url_decorator(self, pattern):
        """
        Return the appropriate decorator for the view function with the passed
        URL name. Mainly used for access-protecting views.

        It's possible to specify:

        - no permissions necessary: use None
        - a set of permissions: use a list
        - two set of permissions (`or`): use a two-tuple of lists

        See permissions_required decorator for details
        """

        from champsquarebackend.views.decorators import permissions_required
        permssions = self.get_permissions(pattern.name)
        if permssions:
            return permissions_required(permssions, login_url=self.login_url)

    @property
    def urls(self):
        # we get the application and instance namespace here
        return self.get_urls(), self.label, self.namespace

class AppConfig(AppConfigMixin, DjangoAppConfig):
    """
        Base app configuration

        This is subclassed by each app to provide a customizable container
        for its configuration, URL configurations, and permssions
    """

class AppDashboardConfig(AppConfig):
    login_url = reverse_lazy('dashboard:login')






        



