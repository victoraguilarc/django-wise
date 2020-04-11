# -*- coding: utf-8 -*-

import pytest
from rest_framework import status
from django.urls import reverse
from apps.accounts import response_codes
from apps.accounts.models.choices import ActionCategory
from apps.accounts.tests.conftest import TEST_PASSWORD
from apps.contrib.utils.tests.unit_tests import mail_outbox, has_response_format, has_unauthorized
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
        assert response_json['code'] == response_codes.RESET_PASSWORD_SENT['code']
        assert mail_outbox() == 1

    def test_reset_password_username(self, api_client, test_user):
        self.assert_reset_password(api_client, {'user': test_user.username})

    def test_reset_password_email(self, api_client, test_user):
        self.assert_reset_password(api_client, {'user': test_user.email})

    def test_reset_password_required_fields(self, api_client):
        response = api_client.post(self.reset_password_url)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'user' in response_json
        assert isinstance(response_json['user'], list)
        assert len(response_json['user']) > 0
        assert response_json['user'][0]['code'] == 'required'

    def test_reset_password_with_redirect_uri(self, api_client, test_user):
        self.assert_reset_password(
            api_client,
            {'user': test_user.email, 'redirect_uri': 'http://localhost:8000/reset-password'},
        )

    def test_reset_password_non_existent_user(self, api_client):
        response = api_client.post(
            self.reset_password_url,
            data={'user': 'ANYTHING'},
        )
        response_json = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert has_response_format(response)
        assert response_json['code'] == response_codes.USER_NOT_FOUND['code']

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
        assert response_json['code'] == response_codes.PASSWORD_UPDATED['code']

    def test_confirm_reset_password___required_fields(self, api_client):
        response = api_client.post(self.confirm_reset_password_url)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert {'token', 'password'} <= set(response_json.keys())
        assert response_json['token'][0]['code'] == 'required'
        assert response_json['password'][0]['code'] == 'required'

    def test_confirm_reset_password__invalid_token(self, api_client):
        response = api_client.post(
            self.confirm_reset_password_url,
            data={'token': 'anything', 'password': 'password'},
        )
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert has_response_format(response)
        assert response_json['code'] == response_codes.INVALID_TOKEN['code']

    def test_set_password__usable_password(self, auth_api_client):
        data = {'password': self.new_test_password, 'confirm_password': self.new_test_password}
        response = auth_api_client.post(self.password_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response_json
        assert response_json['password'][0]['code'] == response_codes.USER_HAS_PASSWORD['code']

    def test_set_password__credentials_required(self, api_client):
        response = api_client.post(self.password_url)
        assert has_unauthorized(response)

    def test_set_password__unusable_pasword(self, auth_api_client, test_user):
        test_user.password = '!unusable_password'  # noqa
        test_user.save()

        data = {'password': self.new_test_password, 'confirm_password': self.new_test_password}
        response = auth_api_client.post(self.password_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert has_response_format(response)
        assert response_json['code'] == response_codes.PASSWORD_ADDED['code']

    def test_set_password__required_fields(self, auth_api_client):
        response = auth_api_client.post(self.password_url)
        response_json = response.json()
        assert {'password', 'confirm_password'} <= set(response_json.keys())
        assert response_json['password'][0]['code'] == 'required'
        assert response_json['confirm_password'][0]['code'] == 'required'

    def test_set_password__password_mismatch(self, auth_api_client, test_user):
        test_user.password = '!unusable_password'  # noqa
        test_user.save()

        data = {'password': self.new_test_password, 'confirm_password': 'anything'}
        response = auth_api_client.post(self.password_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response_json
        assert response_json['errors'][0]['code'] == response_codes.PASSWORD_MISTMATCH['code']

    def test_change_password(self, auth_api_client):
        data = {
            'password': TEST_PASSWORD,
            'new_password': 'anything',
            'confirm_password': 'anything',
        }
        response = auth_api_client.put(self.password_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert has_response_format(response)
        assert response_json['code'] == response_codes.PASSWORD_UPDATED['code']

    def test_change_password__required_fields(self, auth_api_client):
        response = auth_api_client.put(self.password_url)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert {'password', 'new_password', 'confirm_password'} <= set(response_json.keys())
        assert response_json['password'][0]['code'] == 'required'
        assert response_json['new_password'][0]['code'] == 'required'
        assert response_json['confirm_password'][0]['code'] == 'required'

    def test_change_password__credentials_required(self, api_client):
        data = {
            'password': TEST_PASSWORD,
            'new_password': 'anything',
            'confirm_password': 'anything',
        }
        response = api_client.put(self.profile_url, data)
        assert has_unauthorized(response)

    def test_change_password__wrong_current_password(self, auth_api_client):
        data = {
            'password': 'anything',
            'new_password': 'anything',
            'confirm_password': 'anything',
        }
        response = auth_api_client.put(self.password_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response_json
        assert response_json['password'][0]['code'] == response_codes.INVALID_PASSWORD['code']

    def test_change_password__password_mismatch(self, auth_api_client):
        data = {
            'password': TEST_PASSWORD,
            'new_password': 'anything',
            'confirm_password': 'other_thing',
        }
        response = auth_api_client.put(self.password_url, data, is_authenticated=True)
        response_json = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response_json
        assert response_json['errors'][0]['code'] == response_codes.PASSWORD_MISTMATCH['code']
