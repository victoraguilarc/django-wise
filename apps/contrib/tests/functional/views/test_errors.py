# -*- coding: utf-8 -*-

from django.test import override_settings
from rest_framework import status

from apps.contrib.views.errors import error400, error403, error404, error500


@override_settings(DEBUG=True)
def test_error400(rf):
    request = rf.get('/400/')
    response = error400(request)
    assert response.status_code == status.HTTP_200_OK


@override_settings(DEBUG=True)
def test_error403(rf):
    request = rf.get('/403/')
    response = error403(request)
    assert response.status_code == status.HTTP_200_OK


@override_settings(DEBUG=True)
def test_error404(rf):
    request = rf.get('/404/')
    response = error404(request)
    assert response.status_code == status.HTTP_200_OK


@override_settings(DEBUG=True)
def test_error500(rf):
    request = rf.get('/500/')
    response = error500(request)
    assert response.status_code == status.HTTP_200_OK
