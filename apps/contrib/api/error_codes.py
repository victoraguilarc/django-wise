# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from apps.contrib.api.exceptions.base import APINotAuthenticated, APIAuthenticationFailed


class ErrorCodes(object):
    INVALID_TOKEN = APINotAuthenticated(
        code='users.InvalidToken',
        detail=_('Invalid or Expired token'),
    )
    AUTHENTICATION_FAILED = APIAuthenticationFailed(
        code='users.AuthenticationFailed',
        detail=_('Authentication Fails'),
    )
