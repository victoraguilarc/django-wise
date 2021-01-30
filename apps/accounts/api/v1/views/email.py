# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts import response_codes
from apps.contrib.api.responses import DoneResponse
from apps.accounts.models.choices import ActionCategory
from apps.accounts.serializers.login import UsernameOrEmailSerializer
from apps.accounts.serializers.token import TokenSerializer
from apps.accounts.services.auth_service import AuthService
from apps.accounts.selectors.user_selector import UserSelector
from apps.accounts.selectors.pending_action_selector import PendingActionSelector


class EmailActionsViewSet(ViewSet):
    """Contains email confirmation endpoints."""

    permission_classes = [AllowAny]
    permissions_by_action = {
        'update_email': [IsAuthenticated],
    }

    DJANGO_BACKEND = 'django'

    def email_confirmation_request(self, request):
        """Requests a confirmation email."""
        serializer = UsernameOrEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data['user']
        user = UserSelector.get_by_username_or_email(username_or_email)

        if user.is_active:
            return DoneResponse(
                **response_codes.EMAIL_VERIFIED,
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            AuthService.send_confirmation_email(user)
            return DoneResponse(**response_codes.CONFIRMATION_EMAIL_SENT)

    def email_confirmation(self, request):
        """Confirms an email."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pending_action = PendingActionSelector.get_by_token(
            token=serializer.validated_data['token'],
            category=ActionCategory.CONFIRM_EMAIL.value,
        )
        AuthService.confirm_email(pending_action)
        return DoneResponse(**response_codes.EMAIL_VERIFIED)
