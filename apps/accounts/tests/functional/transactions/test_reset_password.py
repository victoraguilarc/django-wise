# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse
from rest_framework import status

from apps.accounts.models import PendingAction
from apps.accounts.models.choices import ActionCategory
from apps.accounts.tests.factories.pending_action import PendingActionFactory


@pytest.mark.django_db
class ResetPasswordTests:

    @classmethod
    def make_reset_password_url(cls, token):
        return reverse(
            'accounts:reset-password',
            kwargs={'token': token}
        )

    @classmethod
    def make_pending_action(cls):
        return PendingActionFactory(category=ActionCategory.RESET_PASSWORD.value)

    def test_get_valid_token(self, client):
        pending_action = self.make_pending_action()
        response = client.get(self.make_reset_password_url(pending_action.token))

        assert response.status_code == status.HTTP_200_OK
        assert 'pending_action' in response.context
        assert isinstance(response.context['pending_action'], PendingAction)
        assert response.context['pending_action'] == pending_action

    def test_get_invalid_token(self, client):
        response = client.get(self.make_reset_password_url('invalid_token'))
        assert response.status_code == status.HTTP_200_OK
        assert 'pending_action' in response.context
        assert response.context['pending_action'] is None

    def test_post_valid_token_and_valid_form(self, client):
        pending_action = self.make_pending_action()
        plain_password = 'new_pasword'

        response = client.post(
            self.make_reset_password_url(pending_action.token),
            {'password1': plain_password, 'password2': plain_password},
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'pending_action' in response.context
        assert isinstance(response.context['pending_action'], PendingAction)
        pending_action.user.refresh_from_db()
        assert pending_action.user.check_password(plain_password)

    def test_post_valid_token_and_invalid_form(self, client):
        pending_action = self.make_pending_action()
        plain_password = 'one-password'
        response = client.post(
            self.make_reset_password_url(pending_action.token),
            {'password1': plain_password, 'password2': 'two-password'}
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'pending_action' in response.context
        assert isinstance(response.context['pending_action'], PendingAction)
        assert not pending_action.user.check_password(plain_password)

    def test_post_invalid_token(self, client):
        response = client.post(self.make_reset_password_url('invalid_token'))
        assert response.status_code == status.HTTP_200_OK
        assert 'pending_action' in response.context
        assert response.context['pending_action'] is None
