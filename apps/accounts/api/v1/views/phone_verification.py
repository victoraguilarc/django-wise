# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.services.one_time_service import OTPService
from apps.accounts.serializers.phone_verification_serializer import (
    PhoneVerificationSerializer, PendingPhoneVerificationSerializer, RequestPhoneVerificationSerializer,
)


class PhoneVerification(APIView):
    """Process a google token_id login."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """It register an pending action to verify phone number and send a sms with the required code."""
        serializer = RequestPhoneVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = str(serializer.validated_data.get('phone_number'))
        pending_action = OTPService.request_code_verification(
            user=request.user,
            phone_number=phone_number,
        )
        return Response(PendingPhoneVerificationSerializer(pending_action).data)

    def put(self, request, *args, **kwargs):
        """It takes de verification code and store user phone number."""
        serializer = PhoneVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'status': serializer.validated_data})
