# -*- coding: utf-8 -*-

# Caching
# https://docs.djangoproject.com/en/2.2/topics/cache/
from config.settings.components import env

REDIS_CACHE_URL = env('REDIS_CACHE_URL', default='redis://redis:6379/0')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}
