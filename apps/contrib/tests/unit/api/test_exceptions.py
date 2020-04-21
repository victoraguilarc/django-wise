# -*- coding: utf-8 -*-

from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from apps.contrib.api.exceptions import SimpleJWTExceptionParser


def test_invalid_token_format():
    received_exc = InvalidToken()
    exc = SimpleJWTExceptionParser.parse(received_exc)
    assert isinstance(exc, NotAuthenticated)


def test_authentication_failed_format():
    received_exc = AuthenticationFailed()
    exc = SimpleJWTExceptionParser.parse(received_exc)
    assert isinstance(exc, NotAuthenticated)


def test_another_exception_format():
    received_exc = ValidationError()
    exc = SimpleJWTExceptionParser.parse(received_exc)
    assert type(received_exc) == type(exc)
