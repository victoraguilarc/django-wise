# -*- coding: utf-8 -*-
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.accounts.models import PendingAction


class RequestPhoneVerificationSerializer(serializers.Serializer):
    """Process the phone device information."""

    phone_number = PhoneNumberField()


class PhoneVerificationSerializer(serializers.Serializer):
    """Process the phone device information."""

    pending_action = serializers.CharField()
    verification_code = serializers.CharField(max_length=6)


class PendingPhoneVerificationSerializer(object):
    """Process the phone device information."""

    def __init__(self, pending_action: PendingAction):
        self.pending_action = pending_action

    @property
    def data(self):
        return {
            'pending_action': self.pending_action.uuid,
        }
