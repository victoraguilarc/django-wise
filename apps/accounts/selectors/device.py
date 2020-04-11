# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound

from apps.accounts.models import PhoneDevice
from apps.accounts.response_codes import DEVICE_NOT_FOUND


class PhoneDeviceSelector:
    """Contains all utility methods to help phone device precesses."""

    @classmethod  # noqa: WPS114
    def get_by_uuid(cls, uuid):
        """Get ans instance or raise an API exception."""
        try:
            return PhoneDevice.objects.get(uuid=uuid)
        except (PhoneDevice.DoesNotExist, ValidationError):
            raise NotFound(**DEVICE_NOT_FOUND)
