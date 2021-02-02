# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer


class TokenSerializer(Serializer):
    """Serializer to request and validate a confirmation token."""
    token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

