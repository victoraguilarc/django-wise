# -*- coding: utf-8 -*-
from config.settings.components import env

CONSTANCE_CONFIG = {
    'REGISTER_REQUIRES_EMAIL_CONFIRMATION': (
        True, 'The registering requires email confirmation',
    ),
    'OTP_VALIDATION_URL': (
        '', 'It helps to format OTP SMSs',
    ),
}
CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
CONSTANCE_REDIS_CONNECTION = env('REDIS_CACHE_URL', default='redis://redis:6379/0')
