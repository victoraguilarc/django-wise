# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, _get_error_details, NotAuthenticated  # noqa: WPS436

from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from apps.accounts.response_codes import INVALID_TOKEN, AUTHENTICATION_FAILED


class SimpleValidationError(APIException):
    """Base class to raise API exceptions."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None, message=None):  # noqa: D107
        detail = detail or message or self.default_detail
        code = code or self.default_code

        self.detail = _get_error_details(detail, code)


class SimpleJWTExceptionParser(object):

    @classmethod
    def parse(cls, exc):

        new_exc = exc
        if isinstance(exc, InvalidToken):
            new_exc = NotAuthenticated(**INVALID_TOKEN)
        elif isinstance(exc, AuthenticationFailed):
            new_exc = NotAuthenticated(**AUTHENTICATION_FAILED)
        return new_exc


class ServerError(APIException):
    """Internal server API exception."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Server error')
    default_code = 'internal_server_error'


def formatted_exception_handler(exc, context):
    """Returns custom formatted response for each exception."""

    exc = SimpleJWTExceptionParser.parse(exc)

    response = exception_handler(exc, context)
    if response is not None:
        response.data = exc.get_full_details()  # noqa: WPS110
    return response
