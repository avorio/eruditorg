"""
Django settings for erudit project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from pathlib import Path

from celery.schedules import crontab

DEBUG = True
COMPRESS_ENABLED = True

BASE_DIR = Path(__file__)
ROOT_DIR = BASE_DIR.parents[3]

STATIC_ROOT = str(ROOT_DIR / 'static')
MEDIA_ROOT = str(ROOT_DIR / 'media')
UPLOAD_ROOT = str(ROOT_DIR / 'media' / 'uploads')

# URL of the admin page
ADMIN_URL = 'admin/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

SECRET_KEY = 'INSECURE'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # Érudit apps
    'base',
    'erudit',
    'apps.public.book',
    'apps.public.citations',
    'apps.public.journal',
    'apps.public.search',
    'apps.public.thesis',
    'apps.userspace',
    'apps.userspace.journal',
    'apps.userspace.journal.authorization',
    'apps.userspace.journal.editor',
    'apps.userspace.journal.information',
    'apps.userspace.journal.royalty_reports',
    'apps.userspace.journal.subscription',
    'apps.userspace.library',
    'apps.userspace.library.authorization',
    'apps.userspace.library.members',
    'apps.userspace.library.stats',
    'apps.userspace.library.subscription_ips',
    'apps.userspace.reporting',
    'core.authorization',
    'core.accounts',
    'core.citations',
    'core.editor',
    'core.journal',
    'core.metrics',
    'core.reporting',
    'core.royalty_reports',
    'core.subscription',

    # Third-party apps
    'modeltranslation',
    'polymorphic',
    'post_office',
    'taggit',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third-party apps
    'account_actions',
    'resumable_uploads',
    'django_filters',
    'rules',
    'ckeditor',
    'raven.contrib.django.raven_compat',
    'django_fsm',
    'easy_pjax',
    'django_js_reverse',
    'widget_tweaks',
    'rest_framework',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    str(ROOT_DIR / 'eruditorg' / 'static' / 'build'),
    str(ROOT_DIR / 'eruditorg' / 'static'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'base.middleware.LanguageCookieMiddleware',
    'core.subscription.middleware.SubscriptionMiddleware',
    'core.citations.middleware.SavedCitationListMiddleware',
)

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(ROOT_DIR / 'eruditorg' / 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'base.context_processors.cache_constants',
                'base.context_processors.common_settings',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'builtins': [
                'easy_pjax.templatetags.pjax_tags',
            ],
        },
    },
]


LOGIN_URL = 'public:auth:login'

# Database configuration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eruditorg',
        'USER': 'root',
        'PASSWORD': '',
    }
}

# Cache configuration

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'files': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/erudit_filebased',
    },
}


# Put this in settings.py
POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now',
}

EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = "mail"
EMAIL_PORT = '25'
RENEWAL_FROM_EMAIL = 'admin@localhost'

DEFAULT_FROM_EMAIL = 'ne-pas-repondre@erudit.org'
TECH_EMAIL = 'tech@erudit.org'
PUBLISHER_EMAIL = 'edition@erudit.org'
COMMUNICATION_EMAIL = 'media@erudit.org'
SUBSCRIPTION_EMAIL = 'client@erudit.org'

WSGI_APPLICATION = 'eruditorg.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr'

LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
)

TIME_ZONE = 'EST'

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
    str(ROOT_DIR / 'locale'),
)

USE_TZ = True

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'core.accounts.backends.EmailBackend',
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'core.accounts.hashers.PBKDF2WrappedAbonnementsSHA1PasswordHasher',
    'core.accounts.hashers.DrupalPasswordHasher',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

INDIVIDUAL_SUBSCRIPTION_SALT = 'sample salt'

# External systems
# -----------------------------------------------------------------------------

# Classic website
FALLBACK_BASE_URL = 'http://retro.erudit.org/'

# Fedora settings
FEDORA_ROOT = 'http://10.1.1.33:8080/fedora'
FEDORA_USER = 'fcAdmin'
FEDORA_PASSWORD = 'fcAdmin'

# Solr settings
SOLR_ROOT = 'http://10.1.1.33:8080/solr/eruditpersee/'
SOLR_ADMIN = 'http://10.1.1.33:8080/solr/admin/cores/'

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'userspace.journal.editor': {
            'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "username": "%(username)s", "journal_code": "%(journal_code)s", "message": "%(message)s", "issue_submission": "%(issue_submission)s"}'  # noqa
        }
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

        'userspace.journal.editor.console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'userspace.journal.editor'
        },

        'userspace.journal.editor.file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/userspace.journal.editor.log',
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'userspace.journal.editor',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/errors.log',
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'fedora_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/fedora.log',
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'verbose'
        }

    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'apps.userspace.journal.editor.views': {
            'level': 'DEBUG',
            'handlers': ['userspace.journal.editor.console', ],
            'propagate': False,
        },
        'core.subscription.management.commands.check_ongoing_restrictions': {
            'level': 'DEBUG',
            'handlers': ['console', 'error_file', ],
            'propagate': False,
        },
        'core': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'core.subscription.middleware': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'erudit.fedora': {
            'level': 'INFO',
            'handlers': ['fedora_file', ],
            'propagate': False,
        }
    },
}

# Raven settings
RAVEN_CONFIG = {
    'dsn': None,
}

# Celery settings
# -----------------------------------

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'EST'
CELERY_TASK_RESULT_EXPIRES = None

CELERYBEAT_SCHEDULE = {
    'issuesubmission-files-removal': {
        'task': 'core.editor.tasks.handle_issuesubmission_files_removal',
        'schedule': crontab(minute=0, hour=0),  # Executed daily at midnight
    },
}

# DRF settings
# -----------------------------------

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend', ),
}

# MailChimp settings
# -----------------------------------

MAILCHIMP_UUID = ""
MAILCHIMP_ACTION_URL = ""


# Django JS reverse settings
# -----------------------------------

JS_REVERSE_INCLUDE_ONLY_NAMESPACES = ['public:citations', 'public:search', ]

# Django-ckeditor settings
# -----------------------------------

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Bold', 'Italic', 'Underline'],
            ['Image', 'NumberedList', 'BulletedList', '-', 'JustifyLeft',
             'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat']
        ]
    }
}


try:
    from .settings_env import *  # noqa
except ImportError:
    pass

try:
    from ..settings_env import *  # noqa
except ImportError:
    pass
