import os
import tempfile

import wagtail
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
    "wagtail",
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
    "wagtail.contrib.settings",
    "wagtail_modeladmin",
    "generic_chooser",
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

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "testdb"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Standard template locations
            os.path.join(os.path.dirname(wagtail.__file__), "admin", "templates"),
            # For modeladmin in Wagtail 6.0+
            os.path.join(
                os.path.dirname(os.path.dirname(wagtail.__file__)),
                "wagtail_modeladmin",
                "templates",
            ),
            # Fallback locations
            os.path.dirname(os.path.dirname(wagtail.__file__)),
        ],
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

# keep files uploaded by the tests out of the working tree
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), "wagtailstreamforms-tests")

LOGIN_URL = reverse_lazy("admin:login")

WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = "tests.ValidFormSettingsModel"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
