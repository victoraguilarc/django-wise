# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer

from apps.accounts.models import User
from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.contrib.api.exceptions.base import SerializerFieldExceptionMixin
from apps.accounts.serializers.login_serializer import UsernameOrEmailSerializer

from django.utils.translation import ugettext_lazy as _

PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length  # noqa: WPS437

user_read_only_fields = (
    'id', 'username', 'date_joined', 'last_login', 'new_email',
    'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
    'email_token', 'token', 'groups', 'user_permissions',
)


class CheckValidPasswordMixin(SerializerFieldExceptionMixin, serializers.Serializer):
    """Validates a password."""

    password = serializers.CharField(
        help_text=_('Current password'),
        max_length=PASSWORD_MAX_LENGTH,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = self.context.get('request', None)
        self.user = getattr(self.request, 'user', None)

    def validate_password(self, password):
        if not self.user.check_password(password):
            self.raise_exception(AccountsErrorCodes.INVALID_PASSWORD)
        return password


class PasswordSetSerializer(SerializerFieldExceptionMixin, serializers.Serializer):
    """Validates a password and its confirmation."""

    password = serializers.CharField(
        help_text=_('Current password'),
        max_length=PASSWORD_MAX_LENGTH,
    )

    confirm_password = serializers.CharField(
        help_text=_('New Password'),
        max_length=PASSWORD_MAX_LENGTH,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = self.context['request'].user

    def validate_password(self, password):   # noqa: D102
        if self.user.has_usable_password():
            self.raise_exception(AccountsErrorCodes.USER_HAS_PASSWORD)
        return password

    def validate(self, attrs):  # noqa: D102
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['confirm_password']:
            self.raise_exception(AccountsErrorCodes.PASSWORD_MISTMATCH)
        return attrs


class PasswordUpdateSerializer(CheckValidPasswordMixin):
    """Validates a new password and its confirmation."""

    new_password = serializers.CharField(
        help_text=_('New Password'),
        max_length=PASSWORD_MAX_LENGTH,
    )

    confirm_password = serializers.CharField(
        help_text=_('New Password'),
        max_length=PASSWORD_MAX_LENGTH,
    )

    def validate(self, attrs):  # noqa: D102
        attrs = super().validate(attrs)
        # it's repeated for readability
        if attrs['new_password'] != attrs['confirm_password']:
            self.raise_exception(AccountsErrorCodes.PASSWORD_MISTMATCH)
        return attrs


class PasswordResetSerializer(UsernameOrEmailSerializer):
    """Serializer to request a password reset e-mail."""

    redirect_uri = serializers.URLField(required=False)


class PasswordResetConfirmSerializer(Serializer):
    """Serializer to request and validate password."""

    DEFAULT_PASSWORD_LENGTH = 128
    token = serializers.CharField()
    password = serializers.CharField(max_length=DEFAULT_PASSWORD_LENGTH)
