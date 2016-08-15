""" Settings for running tests """
from .base import *
import logging
logging.disable(logging.CRITICAL)
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environment_variable('DB_NAME'),
        'USER': environment_variable('DB_USER'),
        'PASSWORD': environment_variable('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',       # Set to empty string for default.
    },
    'prodsys': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PASSWORD': environment_variable('DB_PASSWORD'),
        'NAME': 'prodsys_' + environment_variable('DB_NAME'),
        'USER': environment_variable('DB_USER'),
        'HOST': 'localhost',
        'PORT': '5432',       # Set to empty string for default.
    }
}
# EMAIL_BACKEND = django.core.mail.backends.
