# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.models.phone_device import PhoneDevice


class RegisterPhoneDeviceSerializer(serializers.ModelSerializer):
    """Process a phone device registering."""

    def save(self, **kwargs):
        instance = super().save()
        instance.user = self.context['user']
        instance.save()
        return instance

    class Meta:
        model = PhoneDevice
        fields = ['token', 'platform', 'model_name']


class PhoneDeviceSerializer(serializers.ModelSerializer):
    """Process the phone device information."""

    class Meta:
        model = PhoneDevice
        fields = ['uuid', 'created_at', 'token', 'platform', 'model_name', 'is_active']
