# -*- coding: utf-8 -*-

from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts import response_codes
from apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from apps.accounts.models.choices import ActionCategory
from apps.accounts.selectors.pending_action_selector import PendingActionSelector
from apps.accounts.selectors.user_selector import UserSelector
from apps.accounts.services.password import PasswordService
from apps.contrib.api.viewsets import PermissionViewSet
from apps.contrib.api.responses import DoneResponse
from apps.accounts.services.auth import AuthEmailService
from apps.accounts.api.v1.serializers.password import (
    PasswordSetSerializer, PasswordResetSerializer,
    PasswordUpdateSerializer, PasswordResetConfirmSerializer,
)

from django.contrib.auth import update_session_auth_hash


class PasswordActionsViewSet(PermissionViewSet):
    """Contains all accounts endpoints."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    permissions_by_action = {
        'reset_password': [AllowAny],
        'reset_password_confirm': [AllowAny],
    }

    def set_password(self, request):
        """Sets the user password."""
        serializer = PasswordSetSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        plain_password = serializer.validated_data['password']
        PasswordService.set_pasword(request.user, plain_password)

        return DoneResponse(**response_codes.PASSWORD_ADDED)

    def update_password(self, request):
        """Updates the useer passwrod."""
        serializer = PasswordUpdateSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        new_plain_password = serializer.validated_data['new_password']
        PasswordService.set_pasword(request.user, new_plain_password)
        update_session_auth_hash(request, request.user)

        return DoneResponse(**response_codes.PASSWORD_UPDATED)

    def reset_password(self, request):
        """Request a password reset."""

        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data['user']
        user = UserSelector.get_by_username_or_email(username_or_email)

        pending_action = PasswordService.perform_reset_password(user)
        AuthEmailService.send_reset_password(pending_action)

        return DoneResponse(**response_codes.RESET_PASSWORD_SENT)

    def reset_password_confirm(self, request):
        """Confirms a password reset."""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plain_password = serializer.validated_data['password']
        action_token = serializer.validated_data['token']

        pending_action = PendingActionSelector.get_by_token(
            action_token,
            category=ActionCategory.RESET_PASSWORD.value,
        )
        PasswordService.confirm_reset_password(pending_action, plain_password)

        return DoneResponse(**response_codes.PASSWORD_UPDATED)
