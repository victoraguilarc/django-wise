# -*- coding: utf-8 -*-

from django.urls import reverse

import pytest
from doubles import allow, expect
from rest_framework import status

from apps.accounts import response_codes
from apps.accounts.models.choices import ActionCategory
from apps.accounts.services.auth import AuthService
from apps.accounts.tests.factories.pending_action import PendingActionFactory


@pytest.mark.django_db
class EmailActionsViewSetTests:

    email_confirmation_request_url = reverse('api-accounts:v1:email-confirmation-request')
    email_confirmation_url = reverse('api-accounts:v1:email-confirmation')

    def assert_email_confirmation_request(self, api_client, username_or_email):
        response = api_client.post(
            self.email_confirmation_request_url,
            data={'user': username_or_email}
        )
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert {'code', 'message'} <= set(response_json)
        assert response_json['code'] == response_codes.CONFIRMATION_EMAIL_SENT['code']

    def test_email_confirmation_required_fields(self, api_client):
        response = api_client.post(self.email_confirmation_url)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' in response_json
        assert response_json['token'][0]['code'] == 'required'

    def test_email_confirmation_invalid_token(self, api_client):
        response = api_client.post(self.email_confirmation_url, data={'token': 'anything'})
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert {'code', 'message'} <= set(response.json())
        assert response_json['code'] == response_codes.INVALID_TOKEN['code']

    def test_email_confirmation_valid_token(self, api_client):
        allow(AuthService).confirm_email.and_return(True)
        expect(AuthService).confirm_email.once()

        pending_action = PendingActionFactory(category=ActionCategory.CONFIRM_EMAIL.value)
        response = api_client.post(self.email_confirmation_url, data={'token': pending_action.token})
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert {'code', 'message'} <= set(response.json())
        assert response_json['code'] == response_codes.EMAIL_VERIFIED['code']

    def test_email_confirmation_request_username(self, api_client, test_user):
        test_user.is_active = False
        test_user.save()
        self.assert_email_confirmation_request(api_client, test_user.username)

    def test_email_confirmation_request_email(self, api_client, test_user):
        test_user.is_active = False
        test_user.save()
        self.assert_email_confirmation_request(api_client, test_user.email)

    def test_email_confirmation_request_email_verified_email(self, api_client, test_user):
        response = api_client.post(
            self.email_confirmation_request_url,
            data={'user': test_user.email}
        )
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert {'code', 'message'} <= set(response_json)
        assert response_json['code'] == response_codes.EMAIL_VERIFIED['code']

    def test_email_confirmation_request_required_fields(self, api_client):
        response = api_client.post(self.email_confirmation_request_url)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'user' in response_json
        assert response_json['user'][0]['code'] == 'required'

    def test_email_confirmation_request_unexistent_user(self, api_client):
        response = api_client.post(
            self.email_confirmation_request_url,
            data={'user': 'anything'}
        )
        response_json = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert {'code', 'message'} <= set(response_json)
        assert response_json['code'] == response_codes.USER_NOT_FOUND['code']

    def test_email_confirmation_request_confirmated_email(self, api_client, test_user):
        response = api_client.post(
            self.email_confirmation_request_url,
            data={'user': test_user.email},
        )
        response_json = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert {'code', 'message'} <= set(response_json)
        assert response_json['code'] == response_codes.EMAIL_VERIFIED['code']

