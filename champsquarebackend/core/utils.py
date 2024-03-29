import unicodedata
import re
import datetime
import logging
import socket
from subprocess import Popen, PIPE, STDOUT



from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify as django_slugify
from django.shortcuts import resolve_url, redirect
from django.utils.timezone import get_current_timezone, is_naive, make_aware
# from babel.dates import format_timedelta as format_td
from django.template.defaultfilters import date as date_filter
from django.utils.translation import get_language, to_locale

from ipware import get_client_ip

try:
    # Django 3.0 and above
    from django.utils.http import url_has_allowed_host_and_scheme       # noqa F401
except ImportError:
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme


SLUGIFY_RE = re.compile(r'[^\w\s-]', re.UNICODE)


def default_slugifier(value, allow_unicode=False):
    """
     default slugifier function. When unicode is allowed
    it uses Django's slugify function, otherwise it uses cautious_slugify.
    """
    if allow_unicode:
        return django_slugify(value, allow_unicode=True)
    else:
        return cautious_slugify(value)

def cautious_slugify(value):
    """
    Convert a string to ASCII exactly as Django's slugify does, with the exception
    that any non-ASCII alphanumeric characters (that cannot be ASCIIfied under Unicode
    normalisation) are escaped into codes like 'u0421' instead of being deleted entirely.
    This ensures that the result of slugifying e.g. Cyrillic text will not be an empty
    string, and can thus be safely used as an identifier (albeit not a human-readable one).

    cautious_slugify was copied from Wagtail:
    <https://github.com/wagtail/wagtail/blob/8b420b9/wagtail/core/utils.py>

    Copyright (c) 2014-present Torchbox Ltd and individual contributors.
    Released under the BSD 3-clause "New" or "Revised" License
    <https://github.com/wagtail/wagtail/blob/8b420b9/LICENSE>

    Date: 2018-06-15
    """
    # Normalize the string to decomposed unicode form. This causes accented Latin
    # characters to be split into 'base character' + 'accent modifier'; the latter will
    # be stripped out by the regexp, resulting in an ASCII-clean character that doesn't
    # need to be escaped
    value = unicodedata.normalize('NFKD', value)

    # Strip out characters that aren't letterlike, underscores or hyphens,
    # using the same regexp that slugify uses. This ensures that non-ASCII non-letters
    # (e.g. accent modifiers, fancy punctuation) get stripped rather than escaped
    value = SLUGIFY_RE.sub('', value)

    # Encode as ASCII, escaping non-ASCII characters with backslashreplace, then convert
    # back to a unicode string (which is what slugify expects)
    value = value.encode('ascii', 'backslashreplace').decode('ascii')

    # Pass to slugify to perform final conversion (whitespace stripping); this will
    # also strip out the backslashes from the 'backslashreplace' conversion
    return django_slugify(value)

def slugify(value):
    """
    Slugify a string

    The SETTINGS_SLUG_FUNCTION can be set with a dotted path to the slug
    function to use, defaults to 'champsquarebackend.core.utils.default_slugifier'.

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

def safe_referrer(request, default):
    """
    Takes the request and a default URL. Returns HTTP_REFERER if it's safe
    to use and set, and the default URL otherwise.

    The default URL can be a model with get_absolute_url defined, a urlname
    or a regular URL
    """
    referrer = request.META.get('HTTP_REFERER')
    if referrer and url_has_allowed_host_and_scheme(referrer, request.get_host()):
        return referrer
    if default:
        # Try to resolve. Can take a model instance, Django URL name or URL.
        return resolve_url(default)
    else:
        # Allow passing in '' and None as default
        return default

def redirect_to_referrer(request, default):
    """
    Takes request.META and a default URL to redirect to.

    Returns a HttpResponseRedirect to HTTP_REFERER if it exists and is a safe
    URL; to the default URL otherwise.
    """
    return redirect(safe_referrer(request, default))

# def format_timedelta(td):
#     """
#     Takes an instance of timedelta and formats it as a readable translated string
#     """
#     return format_td(
#         td,
#         threshold=2,
#         locale=to_locale(get_language() or settings.LANGUAGE_CODE)
#     )


def format_datetime(dt, format=None):
    """
    Takes an instance of datetime, converts it to the current timezone and
    formats it as a string. Use this instead of
    django.core.templatefilters.date, which expects localtime.

    :param format: Common will be settings.DATETIME_FORMAT or
                   settings.DATE_FORMAT, or the resp. shorthands
                   ('DATETIME_FORMAT', 'DATE_FORMAT')
    """
    if is_naive(dt):
        localtime = make_aware(dt, get_current_timezone())
        logging.warning(
            "champsquarebackend.core.utils.format_datetime received native datetime")
    else:
        localtime = dt.astimezone(get_current_timezone())
    return date_filter(localtime, format)


def datetime_combine(date, time):
    """Timezone aware version of `datetime.datetime.combine`"""
    return make_aware(
        datetime.datetime.combine(date, time), get_current_timezone())

def get_ip_address(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        return None
    return client_ip

def is_ip_address_valid(ip_address):
    if ip_address is None:
        return False
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False

def run_bash_script(command):
    """ runs a bash script using python subprocess module
        command is list of arguments
    """
    if command is None:
        return {"status": "Failed", "output":"Please specify list of commands"}
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        # todo - do a better error catching
        print(str(output))
        if (exitstatus == 0):
            # todo - log the event
            return {"status": "Success", "output":str(output)}
        
        return {"status": "Failed", "output":str(output)}
    except Exception as e:
        return {"status": "Failed", "output":str(e)}
