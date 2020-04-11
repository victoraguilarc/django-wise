# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse

from apps.accounts.emails import ConfirmEmailMessage, ResetPasswordMessage


class AuthEmailService:
    """Contains all utility methods to help email precesses."""

    @classmethod
    def send_confirm_email(cls, pending_action, hostname=settings.PROJECT_HOSTNAME, next_url=None):
        """Sends the confirmation email."""
        confirm_email_url = reverse('accounts:confirm-email', kwargs={'token': pending_action.token})
        action_url = '{hostname}{url}'.format(
            hostname=hostname,
            url=confirm_email_url,
        )
        context = {
            'pending_action': pending_action,
            'action_url': action_url,
            'next_url': next_url,
        }
        ConfirmEmailMessage(context=context).send(to=pending_action.user.email)

    @classmethod
    def send_reset_password(cls, pending_action, hostname=settings.PROJECT_HOSTNAME, next_url=None):
        """Sends the passwor reset email."""
        reset_password_url = reverse('accounts:reset-password', kwargs={'token': pending_action.token})
        action_url = '{hostname}{url}'.format(
            hostname=hostname,
            url=reset_password_url,
        )
        context = {
            'pending_action': pending_action,
            'action_url': action_url,
            'next_url': next_url,
        }
        ResetPasswordMessage(context=context).send(to=pending_action.user.email)
