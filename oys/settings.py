# coding=utf-8

"""
Django settings for oys project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.contrib import messages
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*******'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['site.oys.az', 'oys.az', 'www.oys.az', '192.168.88.175']


# Application definition

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'djcelery',
    'djkombu',

    'lib',
    'common',
    'account',
    'calculator',
    'sale',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'common.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
   # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'crum.CurrentRequestUserMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'oys.urls'

WSGI_APPLICATION = 'oys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oys',
        'USER': 'root',
        'PASSWORD': '012345',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'az'
TIME_ZONE = 'Asia/Baku'
USE_I18N = True
USE_L10N = False
USE_TZ = True

LANGUAGES = (
    ('az', 'Azerbaijani'),
    ('en', 'English'),
    ('ru', 'Russian'),
)

LOCALE_PATHS = (BASE_DIR + '/oys/locale/', )


DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i'
TIME_INPUT_FORMATS = ('%H:%M', '%H:%M:%S')
DATE_INPUT_FORMATS = ('%d.%m.%Y', '%Y-%m-%d')
DATETIME_INPUT_FORMATS = ('%d.%m.%Y %H:%M',)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

STATIC_ROOT = BASE_DIR + '/static/'
MEDIA_ROOT = BASE_DIR + '/media/'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger'
}


ADMINS = (
    ('Степан Дибров', 'dibrovsd@gmail.com'),
    ('Александр Лапшин', 'arquar@gmail.com'),
    ('Кузько Павел', 'pavel.kuzko@gmail.com'),
)

MANAGERS = [email for name, email in ADMINS]

AUTH_USER_MODEL = 'account.User'

ATOMIC_REQUESTS = True

GRAPPELLI_ADMIN_TITLE = u'Система управления'
GRAPPELLI_INDEX_DASHBOARD = 'oys.dashboard.CustomIndexDashboard'


# celery
import djcelery

djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = "database"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

# email
EMAIL_FILE_PATH = MEDIA_ROOT
SERVER_EMAIL = 'no-reply@smart-bp.ru'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_HOST_PASSWORD = '*******'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'oys',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Кэшируем шаблоны, чтоб правка в них не влияла на прод,
# если вдруг нужно править шаблоны на проде
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'suds.client': {
            'handlers': ['file_suds'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
    'handlers': {
        'file_suds': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'oys/logs/suds.log'),
            'formatter': 'format_sm',
        },
    },
    'formatters': {
        'format_sm': {
            'format': '%(asctime)s: %(levelname)s: %(message)s'
        },
    },
}

SITE_ID = 1

ASAN_SVC_URL = 'https://asan.oys.az/site_integration/?wsdl'
ASAN_SVC_USER = '*******'
ASAN_SVC_PWD = '*******'

# Настройки тестовой среды
try:
    from settings_local import *
except Exception as e:
    print u'Ошибка загрузки локальных настроек %s' % e
