# -*- coding: utf-8 -*-

from django.test import override_settings
from rest_framework import status

from apps.contrib.views.errors import error_400, error_403, error_404, error_500


@override_settings(DEBUG=True)
def test_error_400(rf):
    request = rf.get('/400/')
    response = error_400(request)
    assert response.status_code == status.HTTP_200_OK


@override_settings(DEBUG=True)
def test_error_403(rf):
    request = rf.get('/403/')
    response = error_403(request)
    assert response.status_code == status.HTTP_200_OK


@override_settings(DEBUG=True)
def test_error_404(rf):
    request = rf.get('/404/')
    response = error_404(request)
    assert response.status_code == status.HTTP_200_OK


@override_settings(DEBUG=True)
def test_error_500(rf):
    request = rf.get('/500/')
    response = error_500(request)
    assert response.status_code == status.HTTP_200_OK
