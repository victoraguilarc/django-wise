# -*- coding: utf-8 -*-

from django.core import mail
from rest_framework import status


def mail_outbox():
    """It helps to test if any email message was sended."""
    return len(mail.outbox)


def has_same_code(item1, item2):
    """It helps to checl if two responses has the same error code."""
    return (
        isinstance(item1, dict) and
        isinstance(item2, dict) and
        item1.get('code') == item2.get('code')
    )


def assert_validation_code(response_json, attribute, code):
    """Utility to validate the standar error code."""
    assert 'validation' in response_json
    assert attribute in response_json['validation']
    assert response_json['validation'][attribute]
    assert response_json['validation'][attribute][0]['code'] == code


def assert_error_code(response_json, code):
    """Utility to check any error code inside errors."""
    assert 'errors' in response_json
    assert response_json['errors']
    assert response_json['errors'][0]['code'] == code


def has_response_format(response):
    """Checks if a dict has formatted error code."""
    response_json = response.json()
    return list(response_json.keys()) == ['code', 'message']


def assert_unauthorized(response):
    """Checks if the status code is unauthorized."""
    response_json = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert_error_code(response_json, 'not_authenticated')
