# -*- encoding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class SimpleEmailBackend(ModelBackend):
    """It allow to sign-in with email/password in the admin page."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Overrides Backend base method."""
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
