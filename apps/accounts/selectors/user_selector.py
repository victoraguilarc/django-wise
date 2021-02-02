# -*- coding: utf-8 -*-

from django.db.models import Q

from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.models import User


class UserSelector:
    """Contains all utility methods to help phone device precesses."""

    @classmethod
    def get_by_username_or_email(cls, user_or_email):
        """Get ans instance or raise an API exception."""

        try:
            _filter = Q(username=user_or_email) | Q(email=user_or_email)
            return User.objects.get(_filter)
        except User.DoesNotExist:
            raise AccountsErrorCodes.USER_NOT_FOUND
