from os import environ
from os.path import dirname, abspath, join

from django.urls import reverse_lazy

SITE_DIR = dirname(abspath(__file__))


# Security

SECRET_KEY = environ.get('SECRET_KEY', '')

DEBUG = True

ALLOWED_HOSTS = [] + environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # wagtail
    'wagtail.core',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.contrib.redirects',
    'wagtail.contrib.forms',
    'wagtail.sites',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.postgres_search',
    'wagtail.contrib.settings',
    'wagtail.contrib.search_promotions',

    'modelcluster',
    'taggit',

    # app specific
    'captcha',
    'example',
    'wagtailstreamforms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(SITE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'example.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': environ.get('RDS_HOSTNAME'),
        'PORT': environ.get('RDS_PORT'),
        'NAME': environ.get('RDS_DB_NAME'),
        'USER': environ.get('RDS_USERNAME'),
        'PASSWORD': environ.get('RDS_PASSWORD'),
    }
}


# Email

DEFAULT_FROM_EMAIL = 'Django <no_reply@example.com>'
EMAIL_HOST = environ.get('EMAIL_HOST')
EMAIL_PORT = environ.get('EMAIL_PORT')
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


# Authentication

AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = reverse_lazy('admin:login')
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = '/'


# Internationalization

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [
    join(SITE_DIR, "static"),
]
STATIC_URL = "/static/"
MEDIA_URL = "/media/"


# Wagtail

WAGTAIL_SITE_NAME = 'example.com'
