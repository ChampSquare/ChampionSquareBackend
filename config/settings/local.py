from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="260NbC8TFHGiMVhuFINxJzMRUyZGz31FMRo9vdnCDXqflSpMhIjfe5kXIe2PSwqm",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            # 'NAME': 'onlintest',
            'NAME': 'champsquarebackend',
            # 'NAME': 'rahmani_3',
            'USER': 'andy1729',
            'PASSWORD': 'ReleaseTHEServer2520',
            'HOST': 'localhost',
            'PORT': 5432,
            # 'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
            # 'NAME': os.environ.get('DATABASE_NAME', location('db.sqlite')),
            # 'USER': os.environ.get('DATABASE_USER', None),
            # 'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
            # 'HOST': os.environ.get('DATABASE_HOST', None),
            # 'PORT': os.environ.get('DATABASE_PORT', None),
            # 'ATOMIC_REQUESTS': True
        }
    }



# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405
# Celery
# ------------------------------------------------------------------------------
# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "Asia/Kolkata"


# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------
