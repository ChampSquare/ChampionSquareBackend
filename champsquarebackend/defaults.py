from collections import OrderedDict

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _



SETTINGS_WEBSITE_NAME = 'ChampionSquare'
SETTINGS_WEBSITE_TAGLINE = 'An Online Academy'
SETTINGS_HOMEPAGE = '/'

# Dynamic class loading
SETTINGS_DYNAMIC_CLASS_LOADER = 'champsquarebackend.core.loading.default_class_loader'


# Paths
SETTINGS_IMAGE_FOLDER = 'images/products/%Y/%m/'
SETTINGS_DELETE_IMAGE_FILES = True

# Copy this image from static/img to your MEDIA_ROOT folder.
# It needs to be there so Sorl can resize it.
SETTINGS_MISSING_IMAGE_URL = 'image_not_found.jpg'


# Pagination settings

SETTINGS_NOTIFICATIONS_PER_PAGE = 20
SETTINGS_EMAILS_PER_PAGE = 20
SETTINGS_DASHBOARD_ITEMS_PER_PAGE = 10

# Accounts
SETTINGS_ACCOUNTS_REDIRECT_URL = 'user:profile-view'


# Registration
SETTINGS_SEND_REGISTRATION_EMAIL = True
SETTINGS_FROM_EMAIL = 'ujjawalkotafactory@gmail.com'

# Slug handling
SETTINGS_SLUG_FUNCTION = 'champsquarebackend.core.utils.default_slugifier'
SETTINGS_SLUG_MAP = {}
SETTINGS_SLUG_BLACKLIST = []
SETTINGS_SLUG_ALLOW_UNICODE = False

#Cookies
SETTINGS_COOKIES_DELETE_ON_LOGOUT = []



# Hidden features
SETTINGS_HIDDEN_FEATURES = []

# Menu structure of the dashboard navigation
SETTINGS_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Questions'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Questions'),
                'url_name': 'dashboard:questions-list',
            },
            {
                'label': _('Subjects'),
                'url_name': 'dashboard:question-subject-create',
            }
        ]
    },
    {
        'label': _('Test Manager'),
        'icon': 'icon-bullhorn',
        'children': [
            {
                'label': _('Quizzes'),
                'url_name': 'dashboard:quiz-list',
            },
            {
                'label': _('Category'),
                'url_name': 'dashboard:quiz-category-create',
            }
        ]
    },
    {
        'label': _('Monitoring'),
        'icon': 'icon-bullhorn',
        'children': [
            {
                'label': _('Video Room'),
                'url_name': 'dashboard:video-room',
            }
        ]
    },
    {
        'label': _('Records'),
        'icon': 'icon-bar-chart',
        'children': [
            {
                'label': _('Videos'),
                'url_name': 'dashboard:video-list',
            },
            {
                'label': _('Raw Videos'),
                'url_name': 'dashboard:videos',
            }
        ]
    },
    {
        'label': _('Users'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Users List'),
                'url_name': 'dashboard:users-index',
            },
            {
                'label': _('Create User'),
                'url_name': 'dashboard:user-create',
            }
        ]
    },
    {
        'label': _('Content'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            }
        ]
    }
]
SETTINGS_DASHBOARD_DEFAULT_ACCESS_FUNCTION = 'champsquarebackend.apps.dashboard.nav.default_access_fn'  # noqa


SETTINGS_URL_SCHEMA = 'http'

SETTINGS_SAVE_SENT_EMAILS_TO_DB = True

HOMEPAGE_URL = '/'

# janus settings
SETTINGS_VIDEO_RECORD_FOLDER_NAME = '/video_recordings/'
SETTINGS_JANUS_POST_PROCESS_FUNCTION_PATH = '~/janus10/bin/janus-pp-rec'
SETTINGS_JANUS_POST_PROCESS_SCRIPT = 'champsquarebackend/scripts/janus_post_process.sh'
SETTINGS_AUDIO_VIDEO_MERGE_SCRIPT = 'champsquarebackend/scripts/merge_audio_video.sh'
