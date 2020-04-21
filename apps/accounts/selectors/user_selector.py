# -*- coding: utf-8 -*-

from django.db.models import Q
from rest_framework.exceptions import NotFound

from apps.accounts.models import PhoneDevice, User
from apps.accounts.response_codes import USER_NOT_FOUND


class UserSelector:
    """Contains all utility methods to help phone device precesses."""

    @classmethod
    def get_by_username_or_email(cls, user_or_email):
        """Get ans instance or raise an API exception."""

        try:
            _filter = Q(username=user_or_email) | Q(email=user_or_email)
            return User.objects.get(_filter)
        except User.DoesNotExist:
            raise NotFound(**USER_NOT_FOUND)
