# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.services.session_service import SessionService
from apps.accounts.serializers.user_profile_serializer import UserProfileSerializer


class SessionSerializer(object):
    """Serializes user Session."""

    def __init__(self, user):
        self.user = user

    @property
    def data(self):
        return {
            'session': SessionService.make_user_session(self.user),
            'profile': UserProfileSerializer(self.user).data,
        }


class GoogleTokenSerializer(serializers.Serializer):
    """Serializer to get and validate email or user name."""

    token = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    """Serializer to get and validate email or user name."""

    access_token = serializers.CharField()
