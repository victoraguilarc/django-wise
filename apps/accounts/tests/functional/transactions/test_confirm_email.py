# -*- coding: utf-8 -*-

import pytest
from doubles import allow, expect
from django.urls import reverse
from rest_framework import status

from apps.accounts.models.choices import ActionCategory
from apps.accounts.services.auth_service import AuthService
from apps.accounts.tests.factories.pending_action import PendingActionFactory


@pytest.mark.django_db
class ConfirmEmailTests:

    @classmethod
    def make_confirm_email_url(cls, token):
        return reverse(
            'accounts:confirm-email',
            kwargs={'token': token}
        )

    def test_get_with_valid_token(self, api_client):
        pending_action = PendingActionFactory(category=ActionCategory.CONFIRM_EMAIL.value)

        allow(AuthService).confirm_email.and_return(True)
        expect(AuthService).confirm_email.once()

        response = api_client.get(self.make_confirm_email_url(pending_action.token))
        assert response.status_code == status.HTTP_200_OK

    def test_get_without_invalid_token(self, api_client):
        allow(AuthService).confirm_email.and_return(True)
        expect(AuthService).confirm_email.never()

        response = api_client.get(self.make_confirm_email_url('invalid_token'))
        assert response.status_code == status.HTTP_200_OK

