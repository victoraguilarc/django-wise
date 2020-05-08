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


def has_response_format(response):
    response_json = response.json()
    return {'code', 'message'} <= set(response_json.keys())


def has_unauthorized(response):
    response_json = response.json()
    return (
        response.status_code == status.HTTP_401_UNAUTHORIZED and
        has_response_format(response) and
        response_json['code'] == 'not_authenticated'
    )
