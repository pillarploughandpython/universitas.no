"""Development settings and globals."""

from .base import *


########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'localemail@localhost'
########## END EMAIL CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


DATABASES.update( {
    'prodsys': {
        'ENGINE': 'mysql.connector.django',
        'NAME': environ["DJANGO_PRODSYS_DB_NAME"],
        'USER': environ["DJANGO_PRODSYS_DB_USER"],
        'PASSWORD': environ["DJANGO_PRODSYS_DB_PASSWORD"],
        'HOST': environ["DJANGO_PRODSYS_DB_HOST"],
        'PORT': '',       # Set to empty string for default.
    }
})
DATABASE_ROUTERS = ['apps.legacy_db.router.ProdsysRouter']

######### TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    'debug_toolbar',
    'apps.legacy_db',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION