import re

from django.conf import settings


def strip_language_code(request):
    """
    When using Django's i18n_patterns, we need a language-neutral variant of
    the current URL to be able to use set_language to change languages.
    This naive approach strips the language code from the beginning of the URL
    and will likely fail if using translated URLs.
    """
    path = request.path
    if settings.USE_I18N and hasattr(request, 'LANGUAGE_CODE'):
        return re.sub('^/%s/' % request.LANGUAGE_CODE, '/', path)
    return path


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {'website_name': settings.SETTINGS_WEBSITE_NAME,
            'website_tagline': settings.SETTINGS_WEBSITE_TAGLINE,
            'homepage_url': settings.SETTINGS_HOMEPAGE,
            'language_neutral_url_path': strip_language_code(request),
            # Fallback to old settings name for backwards compatibility
            'use_less': (getattr(settings, 'SETTINGS_USE_LESS', None)
                         or getattr(settings, 'USE_LESS', False)),
            'google_analytics_id': (getattr(settings, 'SETTINGS_GOOGLE_ANALYTICS_ID', None)
                                    or getattr(settings, 'GOOGLE_ANALYTICS_ID', None))}
