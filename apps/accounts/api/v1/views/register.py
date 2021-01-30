# -*- coding: utf-8 -*-

from constance import config
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.contrib.api.responses import DoneResponse
from apps.accounts.response_codes import CONFIRMATION_EMAIL_SENT
from apps.accounts.serializers.session import SessionSerializer
from apps.accounts.serializers.register import RegisterSerializer
from apps.accounts.services.auth_service import AuthService
from apps.accounts.services.user_service import UserService


class RegisterView(APIView):
    """Process a google token_id login."""

    def post(self, request):
        """Registers an user using the info."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if config.REGISTER_REQUIRES_EMAIL_CONFIRMATION:
            user = UserService.register_new_user(user_data=serializer.validated_data)
            AuthService.send_confirmation_email(user)
            return DoneResponse(**CONFIRMATION_EMAIL_SENT)
        else:
            user = UserService.register_new_user(user_data=serializer.validated_data)
            return Response(SessionSerializer(user).data)

