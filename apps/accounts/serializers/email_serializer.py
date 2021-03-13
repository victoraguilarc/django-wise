# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer

from apps.accounts.models import User
from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.contrib.api.exceptions.base import SerializerFieldExceptionMixin


class EmailSerializer(SerializerFieldExceptionMixin, Serializer):
    """Serialier to request and validate an email."""

    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise self.raise_exception(AccountsErrorCodes.EMAIL_ALREDY_USED)
        return email
