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

import os
from configparser import ConfigParser

from .base import *

SECRET_KEY = 'your_secret_key'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'flop_database_public_dev',
        'USER': 'flop_user',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LOGGING = {  
    'version': 1,  
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'base': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },        
        'configuration': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },        
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        }
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']

MIDDLEWARE = MIDDLEWARE + ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ['127.0.0.1']


# Get configuration from config.ini
#
#
config_file = ConfigParser()
config_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'config.ini')
# this makes ConfigParser keys case sensitive
config_file.optionxform = str
config_file.read(config_filename)

# Override SECRET_KEY and DEBUG if present in config.ini
if 'general' in config_file:
    SECRET_KEY = config_file['general'].get('SECRET_KEY', SECRET_KEY)
    if 'DEBUG' in config_file['general']:
        DEBUG = config_file.getboolean('general', 'DEBUG')

# Override DATABASES['default'] if present in config.ini
if 'db' in config_file:
    DATABASES['default'].update(config_file['db'])

