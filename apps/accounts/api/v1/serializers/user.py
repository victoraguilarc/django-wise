# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.accounts import response_codes
from apps.accounts.models import User

PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length  # noqa: WPS437

user_read_only_fields = (
    'id', 'username', 'date_joined', 'last_login', 'new_email',
    'password', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
    'email_token', 'token', 'groups', 'user_permissions',
)

class UserUpdateSerializer(serializers.ModelSerializer):
    """It helps to validate the user basic info updating."""

    username = serializers.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = self.context.get('request', None)
        self.user = getattr(self.request, 'user', None)

    def validate_username(self, username):  # noqa: D102
        user_exists = User.objects.filter(username=username).exists()
        if self.user.username != username and user_exists:
            raise ValidationError(**response_codes.USERNAME_UNAVAILABLE)
        return username

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'photo',
        )
