# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from apps.contrib.api.error_codes import ErrorCodes
from apps.contrib.api.exceptions.base import APIBadRequest

from django.utils.translation import ugettext_lazy as _


class ThirdPartyExceptionNormalizer(object):
    """
    This class is a Auth Exception utility.

    Some libraries like Simple JWT raises their own exceptions,
    We are catching them here and raising our own exceptions intead.
    all to keep the same format of errors.
    """

    @classmethod
    def parse(cls, exc):
        """Returns an own managed exception insted JWT third exceptions."""
        new_exc = exc
        if isinstance(exc, InvalidToken):
            return ErrorCodes.INVALID_TOKEN
        elif isinstance(exc, AuthenticationFailed):
            return ErrorCodes.AUTHENTICATION_FAILED
        return new_exc


def get_logic_errors_key():
    """Returns the standar error key."""
    return settings.REST_FRAMEWORK.get('NON_FIELD_ERRORS_KEY', 'errors')


def get_validation_errors_key():
    """Returns the standar validation key."""
    return settings.REST_FRAMEWORK.get('VALIDATION_ERRORS_KEY', 'validation')


def format_error_response(data: dict or list):
    """This formats the error in a standar format."""
    if isinstance(data, dict) and 'code' in data and 'message' in data:
        data = [data]
    response = {}
    errors_key = get_logic_errors_key()
    validation_key = get_validation_errors_key()
    if isinstance(data, list):
        response[errors_key] = data
        response[validation_key] = None
    else:
        validation_error = APIBadRequest(code='bad_request', detail=_('There are validation errors in the request'))
        if errors_key in data:
            response[errors_key] = data.pop(errors_key)
        else:
            response[errors_key] = [validation_error.json()]
        response[validation_key] = data.copy()
    return response


def formatted_error_handler(exc, context):
    """Returns custom formatted response for each API views' exceptions."""
    exc = ThirdPartyExceptionNormalizer.parse(exc)
    if isinstance(exc, APIException):
        response = exception_handler(exc, context)
        if response is not None:
            data = exc.get_full_details()  # noqa: WPS110
            response.data = format_error_response(data)
        return response
    return exception_handler(exc, context)
