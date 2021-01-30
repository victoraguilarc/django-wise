# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from apps.accounts import response_codes
from apps.accounts.models import User


class EmailSerializer(Serializer):
    """Serialier to request and validate an email."""

    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError(**response_codes.EMAIL_ALREDY_USED)
        return email
