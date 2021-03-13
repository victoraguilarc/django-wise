# -*- coding: utf-8 -*-

from constance import config
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accounts.api.account_responses import AccountsResponses
from apps.accounts.services.auth_service import AuthService
from apps.accounts.services.user_service import UserService
from apps.accounts.serializers.session_serializer import SessionSerializer
from apps.accounts.serializers.register_serializer import RegisterSerializer


class RegisterView(APIView):
    """Process a google token_id login."""

    def post(self, request):
        """Registers an user using the info."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if config.REGISTER_REQUIRES_EMAIL_CONFIRMATION:
            user = UserService.register_new_user(user_data=serializer.validated_data)
            AuthService.send_confirmation_email(user)
            return Response(AccountsResponses.CONFIRMATION_EMAIL_SENT)
        else:
            user = UserService.register_new_user(user_data=serializer.validated_data)
            return Response(SessionSerializer(user).data)
