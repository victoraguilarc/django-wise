# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.timezone import utc


def now():
    """Returns timezoned now date."""
    return datetime.utcnow().replace(tzinfo=utc)


def ago(**kwargs):
    """Returns timezoned minus a delta time."""
    return now() - timedelta(**kwargs)


def after(date, **kwargs):
    """Returns timezoned plus a delta time."""
    return date + timedelta(**kwargs)


def local_datetime(instance=None):
    """Injects timezone to a datetime."""
    if instance is None:
        instance = timezone.now()
    return timezone.localtime(instance)


def get_timeslug():
    """Get s slug based on a datetime."""
    return str(timezone.now().timestamp()).replace('.', '')
