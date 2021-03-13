# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer


class TokenSerializer(Serializer):
    """Validates token existence."""

    token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    """Validates refresh_token existence."""

    refresh_token = serializers.CharField()
