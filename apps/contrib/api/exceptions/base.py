# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import APIException, _get_error_details


class APIBaseException(APIException):

    def __init__(self, detail=None, code=None, extra=None):  # noqa: D107
        self.code = code or self.default_code
        self.extra = extra
        self.detail = _get_error_details(detail, code)

    def json(self):
        return {'code': self.code, 'message': self.detail}


class GenericError(APIBaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Server Error')
    default_code = 'server_error'


class APIBadRequest(APIBaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'bad_request'


class APIAuthenticationFailed(APIBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Incorrect authentication credentials.')
    default_code = 'authentication_failed'


class APINotAuthenticated(APIBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'not_authenticated'


class APIPermissionDenied(APIBaseException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')
    default_code = 'permission_denied'


class APINotFound(APIBaseException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Not found.')
    default_code = 'not_found'


class APIMethodNotAllowed(APIBaseException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = _('Method Not Allowed.')
    default_code = 'method_not_allowed'


class SerializerFieldExceptionMixin(object):
    def raise_exception(self, error: APIBaseException):
        raise serializers.ValidationError(
            code=error.code,
            detail=error.detail,
        )
