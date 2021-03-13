# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.api.account_responses import AccountsResponses
from apps.accounts.services.session_service import SessionService
from apps.accounts.serializers.token_serializer import RefreshTokenSerializer


class LogoutView(APIView):
    """Process an api rrest logout."""

    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        """Clear all application sessions."""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SessionService.drop_session(serializer.validated_data['refresh_token'])

        return Response(AccountsResponses.LOGGED_OUT)
