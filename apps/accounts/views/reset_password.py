# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render

from apps.accounts.forms import ResetPasswordForm
from apps.accounts.models.choices import ActionCategory
from apps.accounts.models.pending_action import PendingAction


class ResetPasswordView(View):
    """Process a password reset."""

    def get(self, request, token, **kwargs):
        """Renders the html template to init password reset."""
        context = {}
        try:
            context['pending_action'] = PendingAction.objects.get(
                token=token, category=ActionCategory.RESET_PASSWORD.value,
            )
        except PendingAction.DoesNotExist:
            context['pending_action'] = None
        return render(request, 'transactions/reset_password.html', context)

    def post(self, request, token, **kwargs):
        """Processes password reset."""
        context = {}
        try:
            pending_action = PendingAction.objects.get(
                token=token, category=ActionCategory.RESET_PASSWORD.value,
            )

            context['pending_action'] = pending_action
            user = pending_action.user

            form = ResetPasswordForm(data=request.POST)
            context['form'] = form

            if form.is_valid():
                password = form.cleaned_data['password1']
                user.set_password(password)
                user.save()
                pending_action.delete()
                return render(request, 'transactions/reset_password_done.html', context)

        except PendingAction.DoesNotExist:
            context['pending_action'] = None

        return render(request, 'transactions/reset_password.html', context)
