from django.conf import settings
from django.utils.module_loading import import_string

def slugify(value):
    """
    Slugify a string

    The SETTINGS_SLUG_FUNCTION can be set with a dotted path to the slug
    function to use, defaults to 'oscar.core.utils.default_slugifier'.

    SETTINGS_SLUG_MAP can be set of a dictionary of target:replacement pairs

    SETTINGS_SLUG_BLACKLIST can be set to a iterable of words to remove after
    the slug is generated; though it will not reduce a slug to zero length.
    """
    value = str(value)

    # Re-map some strings to avoid important characters being stripped.  Eg
    # remap 'c++' to 'cpp' otherwise it will become 'c'.
    for k, v in settings.SETTINGS_SLUG_MAP.items():
        value = value.replace(k, v)

    slugifier = import_string(settings.SETTINGS_SLUG_FUNCTION)
    slug = slugifier(value, allow_unicode=settings.SETTINGS_SLUG_ALLOW_UNICODE)

    # Remove stopwords from slug
    for word in settings.SETTINGS_SLUG_BLACKLIST:
        slug = slug.replace(word + '-', '')
        slug = slug.replace('-' + word, '')

    return slug
