# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts import response_codes
from apps.contrib.api.responses import DoneResponse
from apps.accounts.services.session import SessionService
from apps.accounts.api.v1.serializers.token import RefreshTokenSerializer


class LogoutView(APIView):
    """Process an api rrest logout"""
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        """Clear all application sessions."""

        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SessionService.drop_session(serializer.validated_data['refresh_token'])
        return DoneResponse(**response_codes.LOGGED_OUT)
