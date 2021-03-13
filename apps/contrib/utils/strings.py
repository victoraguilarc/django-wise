# -*- coding: utf-8 -*-

import uuid
import hashlib
from django.conf import settings

from apps.contrib.utils.dates import ago, now


def compute_md5_hash(string):
    """Gets md5 digest from a string."""
    md5_hash = hashlib.md5()   # noqa: S303, W291
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()


def get_uuid(limit=10):
    """Gets a limited uuid."""
    uuid_sample = str(uuid.uuid4()).replace('-', '')
    if limit and limit <= len(uuid_sample):
        return (uuid_sample[:limit]).upper()
    return uuid_sample.upper()


def get_lapse():
    """Returns a range of dates."""
    now_date = now()
    days = 7
    if settings.TOKEN_EXPIRATION_DAYS:
        days = settings.TOKEN_EXPIRATION_DAYS
    end_date = ago(days=days)

    return now_date, end_date


def get_hostname(request=None):
    """Calculates the server hostname."""
    hostname = ''
    if request:
        hostname = '127.0.0.1'
        if 'HTTP_HOST' in request.META:
            hostname = request.META.get('HTTP_HOST')

        try:
            has_settings = settings.USE_HTTPS
        except AttributeError:
            has_settings = False

        protocol = 'https' if has_settings else 'http'
        hostname = '{protocol}://{hostname}'.format(
            protocol=protocol,
            hostname=hostname,
        )
    return hostname
