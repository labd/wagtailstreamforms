import os
import re
from django.urls import reverse_lazy

SECRET_KEY = "secret"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sitemaps",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # wagtail
    "wagtail.core",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.users",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.search",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.sites",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "taggit",
    "wagtailstreamforms",
    "tests",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

WAGTAIL_VERSION = re.search("wt[0-9]*", os.environ["TOX_ENV_NAME"])[0]

PRE_WAGTAIL_211_VERSIONS = [
    "wt23",
    "wt24",
    "wt25",
    "wt26",
    "wt27",
    "wt28",
    "wt29",
    "wt210"
]

PRE_WAGTAIL_211 = False

if WAGTAIL_VERSION in PRE_WAGTAIL_211_VERSIONS:
     MIDDLEWARE.append("wagtail.core.middleware.SiteMiddleware")
     PRE_WAGTAIL_211 = True

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "testdb"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ROOT_URLCONF = "tests.urls"

STATIC_URL = "/static/"

LOGIN_URL = reverse_lazy("admin:login")

WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = "tests.ValidFormSettingsModel"
