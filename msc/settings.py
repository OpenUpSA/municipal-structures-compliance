"""
Django settings for msc project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import environ
import os

ROOT_DIR = environ.Path(__file__) - 2
PROJ_DIR = ROOT_DIR.path("msc")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

env = environ.Env()

# GENERAL
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# Fail loudly if not set.
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# Rely on nginx to direct only allowed hosts, allow all for dokku checks to work.
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_json_widget",
    "msc.questionnaire",
    "msc.response",
    "msc.organisation",
    "msc.authentication",
]

AUTH_USER_MODEL = "authentication.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ROOT_URLCONF = "msc.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "msc.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

AUTHENTICATION_BACKENDS = ('msc.authentication.backends.EmailBackend',)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = "/static/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [
    str(PROJ_DIR.path("static")),
    str(ROOT_DIR.path("assets/bundles")),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WHITENOISE_AUTOREFRESH = env.bool("DJANGO_WHITENOISE_AUTOREFRESH", False)


import logging.config

LOGGING_CONFIG = None
logging.config.dictConfig(
    {
        "version": 1,
        # keep logs like django.server ERROR    "GET / HTTP/1.1" 500
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                # exact format is not important, this is the minimum information
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console",},
        },
        "loggers": {
            # root logger
            "": {"level": "INFO", "handlers": ["console"],},
        },
    }
)

QUESTION_INPUT_TYPES = tuple([(d, d.capitalize()) for d in [
    "dropdown",
    "shorttext",
    "longtext",
    "checkbox",
    "radio",
    "number"
]])

DEFAULT_INPUT_OPTIONS = {
    "dropdown": {
        "choices": [],
        "validations": {},
        "placeholder": "",
        "response_type": "str"
    },
    "shorttext": {
        "validations": {},
        "placeholder": "",
        "response_type": "str"
    },
    "longtext": {
        "validations": {},
        "placeholder": "",
        "response_type": "str"
    },
    "checkbox": {
        "choices": [],
        "validations": {},
        "placeholder": "",
        "response_type": "list"
    },
    "radio": {
        "choices": ["Yes", "No"],
        "validations": {},
        "placeholder": "",
        "response_type": "list"
    },
    "number": {
        "validations": {},
        "placeholder": "",
        "response_type": "int"
    }
}

LOGIC_ACTION = (
    ("make_required", "Make Required"),
    ("show", "Show"),
    ("hide", "Hide")
)

LOGIC_WHEN = (
    ("answered", "target is answered"),
    ("parent", "parent is answered"),
    ("parent_value", "parent response is equal to"),
    ("target_value", "target response is equal to"),
)

SHARER_RELATIONSHIP_TYPES = tuple([(d, d.capitalize()) for d in [
    "creator",
    "admin",
    "viewer",
]])

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


TAG_MANAGER_ENABLED = env.bool("TAG_MANAGER_ENABLED", False)
if TAG_MANAGER_ENABLED:
    TAG_MANAGER_CONTAINER_ID = env("TAG_MANAGER_CONTAINER_ID")
