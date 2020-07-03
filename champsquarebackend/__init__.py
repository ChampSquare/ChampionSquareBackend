# Use 'alpha', 'beta', 'rc' or 'final' as the 4th element to indicate release type.
VERSION = (0, 0, 1, 'alpha')


def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        version = '%s%s' % (version, mapping[VERSION[3]])
        if len(VERSION) == 5:
            version = '%s%s' % (version, VERSION[4])
    return version


DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
    'django.contrib.flatpages',
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    'ckeditor',
    'ckeditor_uploader',
    'django_tables2',
    'widget_tweaks',
]

LOCAL_APPS = [
    # "champsquarebackend.legacy.Uscholar.apps.UscholarConfig",
    # "champsquarebackend.legacy.Unicorn",
    # "champsquarebackend.legacy.JeeMain",
    "champsquarebackend.config.OnlineTestPlatform",
    "champsquarebackend.apps.user.apps.UserConfig",
    "champsquarebackend.apps.question.apps.QuestionConfig",
    "champsquarebackend.apps.quiz.apps.QuizConfig",
    "champsquarebackend.apps.communication.apps.CommunicationConfig",
    "champsquarebackend.apps.dashboard.apps.DashboardConfig",
    'champsquarebackend.apps.dashboard.questions.apps.QuestionsDashboardConfig',
    'champsquarebackend.apps.dashboard.users.apps.UsersDashboardConfig',
    'champsquarebackend.apps.dashboard.pages.apps.PagesDashboardConfig',
    'champsquarebackend.apps.dashboard.communications.apps.CommunicationsDashboardConfig',

    


    # Your stuff: custom apps go here
]

# Apps that were required for old version to work
# will be removed when new version will start working
LEGACY_SUPPORT_APPS = [
    # third party
    "import_export",
    "easy_thumbnails",
    "taggit",
    
    # local ones
    
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + LEGACY_SUPPORT_APPS


default_app_config = 'champsquarebackend.config.OnlineTestPlatform'
