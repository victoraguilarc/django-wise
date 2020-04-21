# -*- coding: utf-8 -*-

import pytest
from django.urls import reverse
from doubles import allow
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, NotFound

from apps.accounts.api.v1.serializers.session import SessionSerializer
from apps.accounts.response_codes import INVALID_CREDENTIALS, USER_NOT_FOUND, INACTIVE_ACCOUNT
from apps.accounts.selectors.user_selector import UserSelector
from apps.accounts.services.session import SessionService
from apps.accounts.tests.conftest import TEST_PASSWORD


@pytest.mark.django_db
class LoginTests:

    test_url = reverse('api-accounts:v1:login')

    def test_user_not_found(self, api_client):
        allow(UserSelector).get_by_username_or_email.and_raise(NotFound(**USER_NOT_FOUND))

        data = {'user': 'anybody@xiberty.com', 'password': 'anything'}
        response = api_client.post(self.test_url, data)
        response_json = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_json.get('code') == USER_NOT_FOUND.get('code')

    def test_invalid_credentials(self, api_client, test_user):
        allow(UserSelector).get_by_username_or_email.and_return(test_user)
        allow(SessionService).validate_session.and_raise(NotAuthenticated(**INVALID_CREDENTIALS))

        data = {'user': test_user.email, 'password': 'anything'}
        response = api_client.post(self.test_url, data)
        response_json = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_json.get('code') == INVALID_CREDENTIALS.get('code')

    def test_user_with_inactive_account(self, api_client, test_user):
        allow(UserSelector).get_by_username_or_email.and_return(test_user)
        allow(SessionService).validate_session.and_raise(NotAuthenticated(**INACTIVE_ACCOUNT))

        data = {'user': test_user.email, 'password': TEST_PASSWORD}
        response = api_client.post(self.test_url, data=data)
        response_json = response.json()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_json.get('code') == INACTIVE_ACCOUNT.get('code')

    def test_get_credentials(self, api_client, test_user):
        allow(UserSelector).get_by_username_or_email.and_return(test_user)
        allow(SessionService).validate_session.and_return(True)

        expected_session = SessionSerializer(user=test_user).data
        data = {'user': test_user.email, 'password': TEST_PASSWORD}
        response = api_client.post(self.test_url, data=data)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert expected_session.keys() == response_json.keys()
