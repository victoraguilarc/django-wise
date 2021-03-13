# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer


class UsernameOrEmailSerializer(Serializer):
    """Serializer to get and validate email or user name."""

    user = serializers.CharField()


class LoginSerializer(UsernameOrEmailSerializer):
    """Serializer to extends some validation to UsernameOrEmailSerializer."""

    password = serializers.CharField(style={'input_type': 'password'})
