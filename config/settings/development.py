# -*- coding: utf-8 -*-

"""Django development settings.

This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""
import os
import socket
from typing import List

from config.settings.components import env
from config.settings.components.common import TEMPLATES, MIDDLEWARE, INSTALLED_APPS

DEBUG = True

ALLOWED_HOSTS: List[str] = ['*']
SECRET_KEY = env('DJANGO_SECRET_KEY', default='development_secret_key')

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

#
#   D J A N G O   D E B U G   T O O L B A R
# https://django-debug-toolbar.readthedocs.io
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)


#
#   M A I L    S E T T I N G S
#
EMAIL_HOST, EMAIL_PORT = 'mailhog', 1025  # Work with MailHog
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Xiberty <info@xiberty.com>')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


#
#   D E B U G G I N G
#
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']  # localhost IP, docker internal IP
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += ['{0}1'.format(ip[:-1])]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def custom_show_toolbar(request):
    """Only show the debug toolbar to users with the superuser flag."""
    return request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    'SHOW_TOOLBAR_CALLBACK': 'config.settings.development.custom_show_toolbar',
}

QUERYCOUNT = {
    'DISPLAY_DUPLICATES': 11,
}

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
CSP_SCRIPT_SRC = ("'self'", 'ajax.googleapis.com')
CSP_IMG_SRC = ("'self'", 'data:')

#
#   T E s T I N G
#
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
