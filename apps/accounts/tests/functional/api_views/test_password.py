# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse
from rest_framework import status

from apps.accounts.models.choices import ActionCategory
from apps.accounts.tests.conftest import TEST_PASSWORD
from apps.accounts.api.error_codes import AccountsErrorCodes
from apps.accounts.api.account_responses import AccountsResponses
from apps.contrib.utils.testing.unit_tests import (
    mail_outbox, assert_error_code, assert_unauthorized, has_response_format, assert_validation_code,
)
from apps.accounts.tests.factories.pending_action import PendingActionFactory


@pytest.mark.django_db
class PasswordActionsViewSetTests:

    reset_password_url = reverse('api-accounts:v1:password-reset')
    confirm_reset_password_url = reverse('api-accounts:v1:password-reset-confirm')
    password_url = reverse('api-accounts:v1:password')
    profile_url = reverse('api-accounts:v1:profile')

    new_test_password = 'new_test_password'

    def assert_reset_password(self, api_client, password_data):
        response = api_client.post(self.reset_password_url, data=password_data)
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert has_response_format(response)
        assert response_json['code'] == AccountsResponses.RESET_PASSWORD_SENT['code']
        assert mail_outbox() == 1

    def test_reset_password_username(self, api_client, test_user):
        self.assert_reset_password(api_client, {'user': test_user.username})

    def test_reset_password_email(self, api_client, test_user):
        self.assert_reset_password(api_client, {'user': test_user.email})

    def test_reset_password_required_fields(self, api_client):
        response = api_client.post(self.reset_password_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='user',
            code='required',
        )

    def test_reset_password_with_redirect_uri(self, api_client, test_user):
        self.assert_reset_password(
            api_client, {'user': test_user.email, 'redirect_uri': 'http://localhost:8000/reset-password'},
        )

    def test_reset_password_non_existent_user(self, api_client):
        response = api_client.post(
            self.reset_password_url,
            data={'user': 'ANYTHING'},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.USER_NOT_FOUND.code,
        )

    def test_confirm_reset_password(self, api_client, test_user):
        pending_action = PendingActionFactory(
            user=test_user,
            category=ActionCategory.RESET_PASSWORD.value,
        )
        response = api_client.post(
            self.confirm_reset_password_url,
            data={'token': pending_action.token, 'password': 'other_password'}
        )
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert has_response_format(response)
        assert response_json['code'] == AccountsResponses.PASSWORD_UPDATED['code']

    def test_confirm_reset_password___required_fields(self, api_client):
        response = api_client.post(self.confirm_reset_password_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='token',
            code='required'
        )
        assert_validation_code(
            response_json=response.json(),
            attribute='password',
            code='required'
        )

    def test_confirm_reset_password__invalid_token(self, api_client):
        response = api_client.post(
            self.confirm_reset_password_url,
            data={'token': 'anything', 'password': 'password'},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.INVALID_TOKEN.code,
        )

    def test_set_password__usable_password(self, auth_api_client):
        data = {'password': self.new_test_password, 'confirmPassword': self.new_test_password}
        response = auth_api_client.post(self.password_url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='password',
            code=AccountsErrorCodes.USER_HAS_PASSWORD.code,
        )

    def test_set_password__credentials_required(self, api_client):
        response = api_client.post(self.password_url)
        assert_unauthorized(response)

    def test_set_password__unusable_pasword(self, auth_api_client, test_user):
        test_user.password = '!unusable_password'  # noqa
        test_user.save()

        data = {'password': self.new_test_password, 'confirmPassword': self.new_test_password}
        response = auth_api_client.post(self.password_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert has_response_format(response)
        assert response_json['code'] == AccountsResponses.PASSWORD_ADDED['code']

    def test_set_password__required_fields(self, auth_api_client):
        response = auth_api_client.post(self.password_url)
        assert_validation_code(
            response_json=response.json(),
            attribute='password',
            code='required',
        )
        assert_validation_code(
            response_json=response.json(),
            attribute='confirmPassword',
            code='required',
        )

    def test_set_password__password_mismatch(self, auth_api_client, test_user):
        test_user.password = '!unusable_password'  # noqa
        test_user.save()

        data = {'password': self.new_test_password, 'confirmPassword': 'anything'}
        response = auth_api_client.post(self.password_url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.PASSWORD_MISTMATCH.code,
        )

    def test_change_password(self, auth_api_client):
        data = {
            'password': TEST_PASSWORD,
            'newPassword': 'anything',
            'confirmPassword': 'anything',
        }
        response = auth_api_client.put(self.password_url, data)
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert has_response_format(response)
        assert response_json['code'] == AccountsResponses.PASSWORD_UPDATED['code']

    def test_change_password__required_fields(self, auth_api_client):
        response = auth_api_client.put(self.password_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='password',
            code='required',
        )
        assert_validation_code(
            response_json=response.json(),
            attribute='newPassword',
            code='required',
        )
        assert_validation_code(
            response_json=response.json(),
            attribute='confirmPassword',
            code='required',
        )

    def test_change_password__credentials_required(self, api_client):
        data = {
            'password': TEST_PASSWORD,
            'newPassword': 'anything',
            'confirmPassword': 'anything',
        }
        response = api_client.put(self.profile_url, data)
        assert_unauthorized(response)

    def test_change_password__wrong_current_password(self, auth_api_client):
        data = {
            'password': 'anything',
            'newPassword': 'anything',
            'confirmPassword': 'anything',
        }
        response = auth_api_client.put(self.password_url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_validation_code(
            response_json=response.json(),
            attribute='password',
            code=AccountsErrorCodes.INVALID_PASSWORD.code,
        )

    def test_change_password__password_mismatch(self, auth_api_client):
        data = {
            'password': TEST_PASSWORD,
            'newPassword': 'anything',
            'confirmPassword': 'other_thing',
        }
        response = auth_api_client.put(self.password_url, data, is_authenticated=True)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert_error_code(
            response_json=response.json(),
            code=AccountsErrorCodes.PASSWORD_MISTMATCH.code,
        )
