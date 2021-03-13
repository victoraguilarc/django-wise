# -*- coding: utf-8 -*-

from apps.contrib.api.exceptions.base import APINotAuthenticated, APIAuthenticationFailed

from django.utils.translation import ugettext_lazy as _


class ErrorCodes(object):
    """This class is a collection of common exceptions."""

    INVALID_TOKEN = APINotAuthenticated(
        code='users.InvalidToken',
        detail=_('Invalid or Expired token'),
    )
    AUTHENTICATION_FAILED = APIAuthenticationFailed(
        code='users.AuthenticationFailed',
        detail=_('Authentication Fails'),
    )
