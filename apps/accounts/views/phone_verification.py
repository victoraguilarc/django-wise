# -*- coding: utf-8 -*-

from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView


class PhoneVerificationView(LoginRequiredMixin, TemplateView):
    """Processes a password reset."""

    template_name = 'transactions/phone_verification.html'
