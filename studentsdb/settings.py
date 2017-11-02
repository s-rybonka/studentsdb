# module os, allow us to work with folders and files
import os

import environ
from django.core.urlresolvers import reverse_lazy

# Build BASE_DIR for project, e.g. (/home/sr/Development/studentsdb).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set up variables with environment
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'Change me'),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_INTERNAL_IPS=(list, []),
    DJANGO_BASE_URL=(str, 'Change me'),
    DJANGO_EMAIL_BACKEND=(str, 'Change me'),
)

# Read env variables from environment
environ.Env.read_env()

# Keep it False on production
DEBUG = env('DJANGO_DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS')
INTERNAL_IPS = env('DJANGO_INTERNAL_IPS')

ROOT_URLCONF = 'studentsdb.urls'
BASE_URL = env('DJANGO_BASE_URL')
LOGIN_REDIRECT_URL = reverse_lazy('groups_list')

AUTH_USER_MODEL = 'accounts.Account'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth' specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third Part apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'bootstrap3',
    'contact_form',
    'djangobower',
    'django_ajax',
    'datetimewidget',
    'debug_toolbar',
    'rosetta',

    # Own Apps
    'students',
    'accounts',
    'core',
    'manager',

    'rules.apps.AutodiscoverRulesConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'utils.django.AssetsFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates').replace('\\', '/')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'students.context_processors.students_processor',
                'students.context_processors.groups_processors',
            ],
            'libraries': {

                'utils.tags': 'utils.tags',
            }
        },
    },
]

WSGI_APPLICATION = 'studentsdb.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/
USE_I18N = True
LANGUAGE_CODE = 'en'
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'UTC'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# allowed languages
LANGUAGES = [
    ('en', 'English'),
    ('uk', 'Ukrainian'),
    ('ru', 'Russian'),
]

# Model Translations
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'uk', 'ru')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Emails settings
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CONTENT_TYPES = ['PNG', 'JPEG']
MAX_UPLOAD_SIZE = 2621440

DEVELOPMENT_FILE = os.path.join(BASE_DIR, 'log/development.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_dev': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'log/development.log',
            'formatter': 'verbose'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/errors.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django.core.mail.backends.console.EmailBackend',
            'formatter': 'verbose',
        },
        'db': {
            'level': 'INFO',
            'class': 'students.handlers.DbLogHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null', 'file_errors', 'db'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file_dev', 'mail_admins', 'db', 'file_errors'],
            'level': 'INFO',
        },
    }
}

# Debug toolbar
# TODO remove it in production
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

SHOW_TOOLBAR_CALLBACK = True

# STATIC AND MEDIA FILES SETTINGS
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# TODO move this settings to .env
# Вказувати абсолютну адрессу
try:
    from studentsdb.local_settings import *
except ImportError:
    pass
