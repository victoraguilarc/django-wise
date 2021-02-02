# -*- coding: utf-8 -*-

from django.core import mail
from rest_framework import status


def mail_outbox():
    return len(mail.outbox)


def has_same_code(item1, item2):
    return (
        isinstance(item1, dict) and
        isinstance(item2, dict) and
        item1.get('code') == item2.get('code')
    )


def assert_validation_code(response_json, attribute, code):
    assert 'validation' in response_json
    assert attribute in response_json['validation']
    assert len(response_json['validation'][attribute]) > 0
    assert response_json['validation'][attribute][0]['code'] == code


def assert_error_code(response_json, code):
    assert 'errors' in response_json
    assert len(response_json['errors']) > 0
    assert response_json['errors'][0]['code'] == code


def has_response_format(response):
    response_json = response.json()
    return {'code', 'message'} <= set(response_json.keys())


def assert_unauthorized(response):
    response_json = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert_error_code(response_json, 'not_authenticated')
