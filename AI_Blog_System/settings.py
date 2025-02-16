"""
Django settings for AI_Blog_System project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os.path
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from .utils import get_languages, get_parler_languages
import logging



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-wuyvap(3mc(y)kyh+qhw&q*yo!(&rx-da&2hq1$yfb5zil4@kx"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",  # Set to DEBUG to see everything
            "class": "logging.StreamHandler",
            "formatter": "detailed",
        },
    },
    "formatters": {
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Log when AI API keys are missing
AI_OPENAI_API_TOKEN = os.getenv("AI_OPENAI_API_TOKEN", "")
AI_DEEPSEEK_API_TOKEN = os.getenv("AI_DEEPSEEK_API_TOKEN", "")

if not AI_OPENAI_API_TOKEN:
    logging.error("🚨 AI_OPENAI_API_TOKEN is missing!")

if not AI_DEEPSEEK_API_TOKEN:
    logging.error("🚨 AI_DEEPSEEK_API_TOKEN is missing!")



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rosetta", # the rosetta app
    "blog",
    "parler",
    "lang_manager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.locale.LocaleMiddleware", # the locale middleware	

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "AI_Blog_System.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "AI_Blog_System.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

LOGIN_URL = "/admin/login/"



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True # the thingy for translators, check it later
USE_TZ = True


# # TODO: make this dynamic based on the langauge app that we will make
# LANGUAGES = [
#     ('en', _('English')),
#     ('ar', _('Arabic')),
#     ('fr', _('French')),

# ]

# # TODO: make this dynamic based on the langauge app, maybe .json? 
# PARLER_LANGUAGES = {
#     None: (
#         {'code': 'en'},
#         {'code': 'ar'},
#         {'code': 'fr'},
#     ),
#     'default': {
#         'fallback': 'en',
#         'hide_untranslated': False,
#     }
# }


LANGUAGES = get_languages()
PARLER_LANGUAGES = get_parler_languages()

LOCALE_PATHS = [
    # BASE_DIR / 'locale',
    os.path.join(BASE_DIR , 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
