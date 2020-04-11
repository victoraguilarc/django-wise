# -*- coding: utf-8 -*-

from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.accounts import response_codes
from apps.accounts.api.v1.serializers.email import EmailSerializer
from apps.accounts.models import User


class RegisterSerializer(EmailSerializer):
    """Serialier to request and validate user basic info."""

    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_username(self, username):
        if username:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists or username in settings.USERNAME_BLACKLIST:
                raise ValidationError(**response_codes.USERNAME_ALREDY_USED)
        return username
