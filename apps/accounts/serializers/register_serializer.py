# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.serializers.email_serializer import EmailSerializer


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
                self.raise_exception(AccountsErrorCodes.USERNAME_ALREDY_USED)
        return username
