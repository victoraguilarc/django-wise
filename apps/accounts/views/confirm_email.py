# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render

from apps.accounts.models.choices import ActionCategory
from apps.accounts.models.pending_action import PendingAction
from apps.accounts.services.auth_service import AuthService


class ConfirmEmailView(View):
    """Renders the email confirmation page."""

    def get(self, request, token, **kwargs):
        """It renders the html template to confirm email."""
        context = {}
        try:
            pending_action = PendingAction.objects.get(
                token=token,
                category=ActionCategory.CONFIRM_EMAIL,
            )
            context['user'] = pending_action.user
            context['next'] = pending_action.extra.get('next')
            AuthService.confirm_email(pending_action)

        except PendingAction.DoesNotExist:
            context['user'] = None

        return render(request, 'transactions/confirm_email.html', context)
