# -*- coding: utf-8 -*-

from rest_framework import status as status_code
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _


class DoneResponse(Response):  # noqa: D107
    """Base class for REST Exceptions based on CEH from @vicobits."""

    def __init__(self, detail=None, code=None, status=None):  # noqa: D107
        response = {
            'message': detail if detail else _('Successful operation!'),
            'code': code if code else 'successful_action',
        }
        status = status or status_code.HTTP_200_OK
        super().__init__(data=response, status=status)
