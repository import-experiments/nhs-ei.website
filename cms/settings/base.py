"""
Django settings for cms project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""


from pathlib import Path

import environ
from django.core.management import utils

# Get variables from the environment
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()
DEBUG = env("DEBUG")

# Build paths inside the project like this: BASE_DIR / 'name_of_path'
PROJECT_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_DIR.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "cms.home",
    "cms.search",
    "cms.categories",
    "cms.posts",
    "cms.blogs",
    "cms.pages",
    "cms.publications",
    "cms.atlascasestudies",
    "cms.core",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtailnhsukfrontend",
    "wagtailnhsukfrontend.settings",
    # importer
    "importer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "cms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "cms.wsgi.application"
# Set a SECRET_KEY in the environment when running multiple instances
SECRET_KEY = env("SECRET_KEY", default=utils.get_random_secret_key())

# Set the environment variable to the correct host when deployed
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[".localhost", "127.0.0.1"])


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": env.db(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.elasticsearch7",
        "TIMEOUT": 5,
        "AUTO_UPDATE": True,
        "URLS": env.list("WAGTAILSEARCH_URLS", default=["http://search:9200"]),
    },
}


# Media files (User uploaded images and documents)
AZURE_CONNECTION_STRING = env("AZURE_CONNECTION_STRING", default=None)
if AZURE_CONNECTION_STRING:
    AZURE_CONTAINER = env("AZURE_CONTAINER")
    DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
else:
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = BASE_DIR / "compiledassets"
STATIC_URL = "/static/"


# Wagtail settings

WAGTAIL_SITE_NAME = "cms"

# Email
EMAIL_CONFIG = env.email_url("EMAIL_URL", default="smtp://user@:password@localhost:25")
SERVER_EMAIL = env("SERVER_EMAIL", default="root@localhost")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="root@localhost")

vars().update(EMAIL_CONFIG)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
        "general": {
            "format": (
                "%(process)-5d %(thread)d %(name)-50s %(levelname)-8s " "- %(message)s"
            ),
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "general",
            "filters": ["require_debug_true"],
        },
        "console_debug_false": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["mail_admins", "console_debug_false"],
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "cms": {"handlers": ["console"], "level": "DEBUG"},
    },
}
