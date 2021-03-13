# -*- coding: utf-8 -*-
from apps.contrib.utils.strings import get_uuid
from apps.accounts.models.choices import ActionCategory
from apps.accounts.models.pending_action import PendingAction
from apps.accounts.services.email_service import AuthEmailService
from apps.accounts.serializers.email_serializer import EmailSerializer


class AuthService:
    """Contains all utility methods to help auth precesses."""

    DEFAULT_TOKEN_LENGHT = 16

    @classmethod
    def send_confirmation_email(cls, user, new_email=None):
        """Process the email confirmation sending."""
        pending_info = {
            'user': user,
            'category': ActionCategory.CONFIRM_EMAIL,
            'token': get_uuid(cls.DEFAULT_TOKEN_LENGHT),
        }

        if new_email:
            serializer = EmailSerializer(data={'email': new_email})
            serializer.is_valid(raise_exception=True)
            pending_info['extra'] = serializer.validated_data

        pending_action, _ = PendingAction.objects.get_or_create(
            user=user, category=ActionCategory.CONFIRM_EMAIL,
            defaults=pending_info,
        )
        AuthEmailService.send_confirm_email(pending_action)

    @classmethod
    def confirm_email(cls, pending_action):
        """Process the email confirmation."""
        user = pending_action.user

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])

        if 'email' in pending_action.extra:
            serializer = EmailSerializer(data=pending_action.extra)
            serializer.is_valid(raise_exception=True)
            user.email = serializer.validated_data['email']
            user.save(update_fields=['email'])
        pending_action.delete()
