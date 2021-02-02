# -*- coding: utf-8 -*-

from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from apps.contrib.api.exceptions.base import APINotAuthenticated, APIAuthenticationFailed
from apps.contrib.api.exceptions.error_handler import ThirdPartyExceptionNormalizer


def test_invalid_token_format():
    received_exc = InvalidToken()
    exc = ThirdPartyExceptionNormalizer.parse(received_exc)
    assert isinstance(exc, APINotAuthenticated)


def test_authentication_failed_format():
    received_exc = AuthenticationFailed()
    exc = ThirdPartyExceptionNormalizer.parse(received_exc)
    assert isinstance(exc, APIAuthenticationFailed)


def test_another_exception_format():
    received_exc = ValidationError()
    exc = ThirdPartyExceptionNormalizer.parse(received_exc)
    assert type(received_exc) == type(exc)
