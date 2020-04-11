# -*- coding: utf-8 -*-

from os.path import join, dirname

from environ import environ

PROJECT_PATH = dirname(dirname(dirname(dirname(__file__))))
APPS_PATH = join(PROJECT_PATH, 'apps')

env = environ.Env()
READ_ENV_FILE = env.bool('DJANGO_READ_ENV_FILE', default=False)
if READ_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env_file = join(PROJECT_PATH, '.env')
    env.read_env(env_file)
