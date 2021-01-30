# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""

    photo = serializers.CharField(source='photo_url')
    has_password = serializers.SerializerMethodField()

    def get_has_password(self, user):
        return user.has_usable_password()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'lang',
            'is_active',
            'has_password',
        )
        read_only_fields = fields
