"""
Django settings for ProjectApplication project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime
import mimetypes
import os
import pathlib
import tempfile

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'simple_history',
    'phonenumber_field',
    'axes',
    'project_core',
    'variable_templates',
    'evaluation',
    'comments',
    'colours',
    'grant_management',
    'reporting'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'project_core.middleware.login.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',

    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # It only formats user lockout messages and renders Axes lockout responses
    # on failed user authentication attempts from login views.
    # If you do not want Axes to override the authentication response
    # you can skip installing the middleware and use your own views.
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'ProjectApplication.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'project_core.processors.navbar_background.background',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjectApplication.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'project_core': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# https://docs.djangoproject.com/en/3.0/ref/settings/#secure-proxy-ssl-header
# Make sure that nginx is doing what's described in the link above
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


def secrets_file(file_name, optional_path=None):
    """ First try optional_path, then $HOME/.file_name, then /run/secrets/file_name, else raises an exception"""

    if optional_path is not None:
        file_path_in_optional = os.path.join(optional_path, file_name)
        if os.path.exists(file_path_in_optional):
            return file_path_in_optional

    file_path_in_home_directory = os.path.join(str(pathlib.Path.home()), "." + file_name)
    if os.path.exists(file_path_in_home_directory):
        return file_path_in_home_directory

    file_path_in_run_secrets = os.path.join("/run/secrets", file_name)
    if os.path.exists(file_path_in_run_secrets):
        return file_path_in_run_secrets

    raise FileNotFoundError("Configuration for {} doesn't exist".format(file_name))


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if os.getenv('FORCE_SQLITE3_DATABASE', False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': secrets_file('project_application_mysql.conf', '/etc/mysql'),
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
            'TEST': {
                'NAME': 'test_projects'
            }
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

cache_directory = os.path.join(tempfile.gettempdir(), 'project-application-cache')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': cache_directory,
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = False

# USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# For deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For the Debugging extension
# management_IPS = [
#     '127.0.0.1',
# ]

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/logged/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Makes message tags compatible with Bootstrap4 alert messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

mimetypes.init()

LOGIN_CONTACT = 'SPI'

AWS_DEFAULT_ACL = 'private'

AWS_ACCESS_KEY_ID = os.environ['OBJECT_STORAGE_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['OBJECT_STORAGE_SECRET_ACCESS_KEY']

AWS_LOCATION = os.environ['OBJECT_STORAGE_PREFIX_LOCATION']

if 'OBJECT_STORAGE_ENDPOINT_URL' in os.environ:
    AWS_S3_ENDPOINT_URL = os.environ['OBJECT_STORAGE_ENDPOINT_URL']

if 'OBJECT_STORAGE_BUCKET_NAME' in os.environ:
    AWS_STORAGE_BUCKET_NAME = os.environ['OBJECT_STORAGE_BUCKET_NAME']

if 'OBJECT_STORAGE_REGION_NAME' in os.environ:
    AWS_S3_REGION_NAME = os.environ['OBJECT_STORAGE_REGION_NAME']

if 'OBJECT_STORAGE_ADDRESSING_STYLE' in os.environ:
    AWS_S3_ADDRESSING_STYLE = os.environ['OBJECT_STORAGE_ADDRESSING_STYLE']

DATE_FORMAT = 'd F Y'
DATETIME_FORMAT = 'd F Y H:i'

SHORT_DATE_FORMAT = 'd-m-Y'
SHORT_DATETIME_FORMAT = 'd-m-Y H:i'

AWS_S3_FILE_OVERWRITE = False

SECRET_KEY = os.environ['SECRET_KEY']

# The usual Django /admin will appear in /$ADMIN_URL_PATH
ADMIN_URL = os.environ['ADMIN_URL_PATH']

ALLOWED_HOSTS = []

i = 1
while f'ALLOWED_HOST_{i}' in os.environ:
    ALLOWED_HOSTS.append(os.environ[f'ALLOWED_HOST_{i}'])
    i += 1

ADMINS = []
i = 1
while f'ADMIN_{i}' in os.environ:
    name_email = os.environ[f'ADMIN_{i}']
    ADMINS.append(name_email.split(','))
    i += 1

DEFAULT_FROM_EMAIL = SERVER_EMAIL = os.environ['FROM_EMAIL']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_SUBJECT_PREFIX = os.environ['EMAIL_SUBJECT_PREFIX']
EMAIL_USE_TLS = True

# This is part of django-axes: lock out users temporary if login fails
# See https://django-axes.readthedocs.io/en/latest/4_configuration.html
AXES_ENABLED = 1
AXES_FAILURE_LIMIT = 10

# Next option would lock out the IP. Not doing it: from the office/NAT a user would be able to lock out all the users
# AXES_LOCK_OUT_AT_FAILURE = False

AXES_COOLOFF_TIME = datetime.timedelta(minutes=5)

AXES_ONLY_USER_FAILURES = True

AXES_LOCKOUT_TEMPLATE = 'registration/user-locked-out-out.tmpl'

DEBUG = os.environ['DEBUG'] == '1'
SECURE_SSL_REDIRECT = os.environ['SECURE_SSL_REDIRECT'] == '1'
SECURE_REFERRER_POLICY = 'same-origin'

if SECURE_SSL_REDIRECT:
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 3600
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

# Project Application specific settings
# These settings are specific by the Project Application code. They are not Django settings
HTTP_AUTH_INCOMING_LINKS = os.getenv('HTTP_AUTH_INCOMING_LINKS', '')
NAVBAR_BACKGROUND_COLOR = os.getenv('NAVBAR_BACKGROUND_COLOR', 'bg-primary')

# This category was used during the importer of Projects that were created before the Project Application existed
# These projects were managed via a Spreadsheet and imported here. Some information (comments, attachments)
# were assigned to DATA_IMPORT_CATEGORY_NAME but users of the application cannot select this category for their
# comments and attachments
DATA_IMPORT_CATEGORY_NAME = 'Data Import'

GOAT_COUNTER_CODE = os.getenv('GOAT_COUNTER_CODE', None)
REVIEWER_GROUP_NAME = 'reviewer'
MANAGEMENT_GROUP_NAME = 'management'

REVIEWER_CAN_ACCESS_VIEW_NAMES = ['logged-proposal-list',
                                  'logged-proposal-detail',
                                  'logged-export-proposals-csv-summary-all',
                                  'logged-export-proposals-csv-summary-call',
                                  'logged-homepage']
LOGGED_OUT_USERNAME = 'loggedout'
PROPOSAL_STATUS_DRAFT = 'Draft'
PROPOSAL_STATUS_SUBMITTED = 'Submitted'
LAY_SUMMARY_ORIGINAL = 'Original'
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
SPI_MEDIA_GALLERY_IMPORT_CALLBACK = os.getenv('SPI_MEDIA_GALLERY_IMPORT_CALLBACK', None)

# This part is created on creating a call
CALL_DEFAULT_PART_QUESTIONS_ANSWERS = 'Proposed {{ activity }} description'