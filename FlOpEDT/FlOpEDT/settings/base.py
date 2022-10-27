# This file is part of the FlOpEDT/FlOpScheduler project.
# Copyright (c) 2017
# Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.
#
# You can be released from the requirements of the license by purchasing
# a commercial license. Buying such a license is mandatory as soon as
# you develop activities involving the FlOpEDT/FlOpScheduler software
# without disclosing the source code of your own applications.

"""
Django settings for FlOpEDT project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from django.utils.translation import gettext_lazy as _

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

#
# Application definition
#

INSTALLED_APPS = [
    'channels',
    'apps.FlOpEDTAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'import_export',
    'colorfield',
    'flopeditor',
    'rest_framework',
    'django_filters',
    'base',
    'TTapp',
    'quote',
    'people',
    'solve_board',
    'ics',
    'displayweb',
    'configuration',
    'easter_egg',
    'MyFlOp',
    #    'importation'
    'api',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_swagger',
    'drf_yasg',
    'corsheaders',
    'cstmanager',
    'notifications',
    'django_crontab',
    'roomreservation',
    'acme_challenge',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.EdtContextMiddleware',
]

ROOT_URLCONF = 'FlOpEDT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.edt_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'FlOpEDT.wsgi.application'
ASGI_APPLICATION = 'FlOpEDT.routing.application'

CACHES = {
   'default': {
       'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       'LOCATION': 'flop',
   }
}

CACHE_COUNT_TIMEOUT = 24 * 3600
CACHE_INVALIDATE_ON_CREATE = 'whole-model'
CACHE_MACHINE_USE_REDIS = True
REDIS_BACKEND = 'redis://127.0.0.1:6379/1'

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
CSRF_USE_SESSION = True
AUTH_USER_MODEL = 'people.User'

# Available languages
LANGUAGES = [
  ('fr', _('French')),
  ('en', _('English')),
  ('es', _('Spanish')),
    ('ar', _('Arabic')),
    ('eu', _('Basque')),
    ('br', _('Breton')),
    ('ca', _('Catalan')),
    ('co', _('Corsican')),
    ('da', _('Danish')),
    ('de', _('German')),
    ('nl', _('Dutch')),
    ('el', _('Greek')),
    ('it', _('Italian')),
    ('la', _('Latin')),
    ('no', _('Norwegian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('sv', _('Swedish')),
    ('zh', _('Chinese')),
    ('sf', _('Smurf'))
]

# Folder which contains traduction files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

#
# ASSETS Settings
#

# Url used by static files in templates
STATIC_URL = '/static/'

# Folder used to store collected static files
STATIC_ROOT = os.path.join(BASE_DIR, "var/static")

# Folders used to find some additional static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#
# EMAIL SETTINGS
#

EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[flop!EDT] '
SERVER_EMAIL = 'no-reply@flop.edt'

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

if 'EMAIL_PORT' in os.environ:
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))

#
# FLOPEDT Settings
#

CUSTOM_CONSTRAINTS_PATH = 'MyFlOp.custom_constraints'

if 'ADMINS' in os.environ:
    ADMINS = [tuple(admin.split(",")) for admin in os.environ.get('ADMINS').split(" ")]
    MANAGERS = ADMINS

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# LOG IN-AND-OUT
LOGIN_REDIRECT_URL = '/backoffice/'
LOGIN_URL = '/'
TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
)

SHELL_PLUS_MODEL_IMPORTS_RESOLVER = 'django_extensions.collision_resolvers.AppLabelSuffixCR'

CORS_ALLOW_ALL_ORIGINS = True
