# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.serializers.user_profile import UserProfileSerializer
from apps.accounts.services.session_service import SessionService


class SessionSerializer(object):

    def __init__(self, user):
        self.user = user

    @property
    def data(self, ):
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

