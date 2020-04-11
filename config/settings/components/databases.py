# -*- coding: utf-8 -*-

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
from config.settings.components import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='postgres'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='postgres'),
        'HOST': env('POSTGRES_HOST', default='postgres'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': env('POSTGRES_CONN_MAX_AGE', default=60),
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    },
}
